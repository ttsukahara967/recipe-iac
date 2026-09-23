from pydantic import BaseModel, ConfigDict


class Ingredient(BaseModel):
    name: str
    amount: str


class RecipeSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    category: str
    cook_time_minutes: int
    servings: int
    image_path: str


class RecipeDetail(RecipeSummary):
    ingredients: list[Ingredient]
    steps: list[str]
