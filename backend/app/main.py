import os
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import String, cast, or_, select, text
from sqlalchemy.orm import Session

from .db import Base, engine, get_session
from .models import Recipe
from .schemas import RecipeDetail, RecipeSummary
from .search import english_terms, query_variants, split_terms
from .seed import seed_recipes


# Schema changes applied after the table first shipped. create_all() never alters an existing
# table, so apply them idempotently on startup (safe on a fresh DB too). The per-locale JSON
# column replaces the earlier *_en columns, which are dropped if present.
_SCHEMA_DDL = (
    "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS translations JSON",
    "ALTER TABLE recipes DROP COLUMN IF EXISTS title_en",
    "ALTER TABLE recipes DROP COLUMN IF EXISTS description_en",
    "ALTER TABLE recipes DROP COLUMN IF EXISTS ingredients_en",
    "ALTER TABLE recipes DROP COLUMN IF EXISTS steps_en",
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Small app, so no migration tool: create tables and upsert seed data on startup
    # Several tasks may start at once, so serialize this with an advisory lock
    with engine.begin() as conn:
        conn.execute(text("SELECT pg_advisory_xact_lock(20260924)"))
        Base.metadata.create_all(conn)
        for ddl in _SCHEMA_DDL:
            conn.execute(text(ddl))
        seed_recipes(conn)
    yield


# Japanese is the base; every other locale is served from the translations JSON, falling back to
# Japanese for any missing field.
Lang = Literal["ja", "en", "zh-Hant", "zh-Hans", "ko"]


def _tr(r: Recipe, lang: Lang) -> dict:
    if lang == "ja":
        return {}
    return (r.translations or {}).get(lang) or {}


def _localize_summary(r: Recipe, lang: Lang) -> dict:
    t = _tr(r, lang)
    return {
        "id": r.id,
        "slug": r.slug,
        # category stays the Japanese key; the frontend maps it to a localized label
        "category": r.category,
        "cook_time_minutes": r.cook_time_minutes,
        "servings": r.servings,
        "image_path": r.image_path,
        "title": t.get("title") or r.title,
        "description": t.get("description") or r.description,
    }


def _localize_detail(r: Recipe, lang: Lang) -> dict:
    d = _localize_summary(r, lang)
    t = _tr(r, lang)
    d["ingredients"] = t.get("ingredients") or r.ingredients
    d["steps"] = t.get("steps") or r.steps
    return d


app = FastAPI(title="Recipe API", lifespan=lifespan)


@app.get("/api/health")
def health():
    return {"status": "ok", "env": os.environ.get("APP_ENV", "local")}


@app.get("/api/categories", response_model=list[str])
def list_categories(session: Session = Depends(get_session)):
    return session.scalars(select(Recipe.category).distinct().order_by(Recipe.category)).all()


@app.get("/api/recipes", response_model=list[RecipeSummary])
def list_recipes(
    category: str | None = None,
    q: str | None = Query(None, max_length=100, description="Keywords matched against title, description, category and ingredients"),
    sort: Literal["default", "new"] = "default",
    limit: int | None = Query(None, ge=1, le=100),
    lang: Lang = "ja",
    session: Session = Depends(get_session),
):
    # Recipes are upserted by slug, so new recipes get new (higher) ids and edits keep theirs:
    # id order is "order added".
    stmt = select(Recipe).order_by(Recipe.id.desc() if sort == "new" else Recipe.id)
    if category:
        stmt = stmt.where(Recipe.category == category)
    if lang == "ja":
        for term in split_terms(q):
            fields = (Recipe.title, Recipe.description, Recipe.category, cast(Recipe.ingredients, String))
            # Every term must match (AND); each term may match any field in any kana form (OR)
            stmt = stmt.where(
                or_(*(field.ilike(f"%{v}%", escape="\\") for v in query_variants(term) for field in fields))
            )
    else:
        # Non-Japanese search: plain case-insensitive substring over that locale's translated
        # subtree (title/description/ingredients/steps). The Japanese kana/synonym logic does
        # not apply. Scoping to translations[lang] avoids matching other locales' text.
        sub = cast(Recipe.translations[lang], String)
        for term in english_terms(q):
            stmt = stmt.where(sub.ilike(f"%{term}%", escape="\\"))
    if limit:
        stmt = stmt.limit(limit)
    return [_localize_summary(r, lang) for r in session.scalars(stmt).all()]


@app.get("/api/recipes/{slug}", response_model=RecipeDetail)
def get_recipe(slug: str, lang: Lang = "ja", session: Session = Depends(get_session)):
    recipe = session.scalar(select(Recipe).where(Recipe.slug == slug))
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return _localize_detail(recipe, lang)
