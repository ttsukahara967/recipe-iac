import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from .db import Base, engine, get_session
from .models import Recipe
from .schemas import RecipeDetail, RecipeSummary
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
def list_recipes(category: str | None = None, session: Session = Depends(get_session)):
    stmt = select(Recipe).order_by(Recipe.id)
    if category:
        stmt = stmt.where(Recipe.category == category)
    return session.scalars(stmt).all()


@app.get("/api/recipes/{slug}", response_model=RecipeDetail)
def get_recipe(slug: str, session: Session = Depends(get_session)):
    recipe = session.scalar(select(Recipe).where(Recipe.slug == slug))
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
