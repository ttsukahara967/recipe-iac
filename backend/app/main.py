import os
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import String, cast, or_, select, text
from sqlalchemy.orm import Session

from .db import Base, engine, get_session
from .models import Recipe
from .schemas import RecipeDetail, RecipeSummary
from .search import query_variants, split_terms
from .seed import seed_recipes


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Small app, so no migration tool: create tables and upsert seed data on startup
    # Several tasks may start at once, so serialize this with an advisory lock
    with engine.begin() as conn:
        conn.execute(text("SELECT pg_advisory_xact_lock(20260924)"))
        Base.metadata.create_all(conn)
        seed_recipes(conn)
    yield


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
    session: Session = Depends(get_session),
):
    # Recipes are upserted by slug, so new recipes get new (higher) ids and edits keep theirs:
    # id order is "order added".
    stmt = select(Recipe).order_by(Recipe.id.desc() if sort == "new" else Recipe.id)
    if category:
        stmt = stmt.where(Recipe.category == category)
    for term in split_terms(q):
        fields = (Recipe.title, Recipe.description, Recipe.category, cast(Recipe.ingredients, String))
        # Every term must match (AND); each term may match any field in any kana form (OR)
        stmt = stmt.where(
            or_(*(field.ilike(f"%{v}%", escape="\\") for v in query_variants(term) for field in fields))
        )
    if limit:
        stmt = stmt.limit(limit)
    return session.scalars(stmt).all()


@app.get("/api/recipes/{slug}", response_model=RecipeDetail)
def get_recipe(slug: str, session: Session = Depends(get_session)):
    recipe = session.scalar(select(Recipe).where(Recipe.slug == slug))
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
