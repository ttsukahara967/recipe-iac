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


# Columns added after the table first shipped. create_all() never alters an existing table,
# so add them idempotently on startup (safe on a fresh DB too).
_ADDED_COLUMNS = (
    "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS title_en VARCHAR(128)",
    "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS description_en TEXT",
    "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS ingredients_en JSON",
    "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS steps_en JSON",
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Small app, so no migration tool: create tables and upsert seed data on startup
    # Several tasks may start at once, so serialize this with an advisory lock
    with engine.begin() as conn:
        conn.execute(text("SELECT pg_advisory_xact_lock(20260924)"))
        Base.metadata.create_all(conn)
        for ddl in _ADDED_COLUMNS:
            conn.execute(text(ddl))
        seed_recipes(conn)
    yield


Lang = Literal["ja", "en"]


def _localize_summary(r: Recipe, lang: Lang) -> dict:
    en = lang == "en"
    return {
        "id": r.id,
        "slug": r.slug,
        # category stays the Japanese key; the frontend maps it to a localized label
        "category": r.category,
        "cook_time_minutes": r.cook_time_minutes,
        "servings": r.servings,
        "image_path": r.image_path,
        "title": (r.title_en or r.title) if en else r.title,
        "description": (r.description_en or r.description) if en else r.description,
    }


def _localize_detail(r: Recipe, lang: Lang) -> dict:
    d = _localize_summary(r, lang)
    en = lang == "en"
    d["ingredients"] = (r.ingredients_en or r.ingredients) if en else r.ingredients
    d["steps"] = (r.steps_en or r.steps) if en else r.steps
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
    if lang == "en":
        # English search: plain case-insensitive substring over the translated fields.
        # The Japanese kana/synonym logic does not apply to English.
        fields = (Recipe.title_en, Recipe.description_en, cast(Recipe.ingredients_en, String))
        for term in english_terms(q):
            stmt = stmt.where(or_(*(field.ilike(f"%{term}%", escape="\\") for field in fields)))
    else:
        for term in split_terms(q):
            fields = (Recipe.title, Recipe.description, Recipe.category, cast(Recipe.ingredients, String))
            # Every term must match (AND); each term may match any field in any kana form (OR)
            stmt = stmt.where(
                or_(*(field.ilike(f"%{v}%", escape="\\") for v in query_variants(term) for field in fields))
            )
    if limit:
        stmt = stmt.limit(limit)
    return [_localize_summary(r, lang) for r in session.scalars(stmt).all()]


@app.get("/api/recipes/{slug}", response_model=RecipeDetail)
def get_recipe(slug: str, lang: Lang = "ja", session: Session = Depends(get_session)):
    recipe = session.scalar(select(Recipe).where(Recipe.slug == slug))
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return _localize_detail(recipe, lang)
