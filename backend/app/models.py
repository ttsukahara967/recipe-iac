from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(32), index=True)
    cook_time_minutes: Mapped[int] = mapped_column(Integer)
    servings: Mapped[int] = mapped_column(Integer)
    image_path: Mapped[str] = mapped_column(String(256))
    ingredients: Mapped[list[dict]] = mapped_column(JSON)
    steps: Mapped[list[str]] = mapped_column(JSON)

    # English translations (nullable). category is not translated here: it stays the Japanese
    # grouping key, and the frontend maps it to a localized label.
    title_en: Mapped[str | None] = mapped_column(String(128), nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    ingredients_en: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    steps_en: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
