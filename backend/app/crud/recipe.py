from backend.app.core.db import AsyncSessionLocal
from backend.app.models import Recipe
from backend.app.schemas.ingredient import Ingredient

from backend.app.schemas.recipe import RecipeCreate



async def create_recipe(
        new_recipe: RecipeCreate,
        session: AsyncSession,
) -> Recipe:
    new_recipe_data = new_recipe.dict()
    db_recipe = Recipe(**new_recipe_data)

    async with AsyncSessionLocal() as session: