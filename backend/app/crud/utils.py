from app.models.model import (
    Recipe, RecipesIngredients, RecipesTags, Favorite,
    ShoppingList, RecipesIngredients, RecipesTags, Tag,
    Ingredient
    )
from app.schemas.recipe import RecipeDB 
from app.crud.recipe import recipe_crud
from app.core.db import AsyncSession
from app.crud.shopping_list import shoppinglist_crud
from app.crud.favorite import favorite_crud


async def set_favorite_shoplist(
        recipes,
        user_id: int,
        session: AsyncSession
):
    if type(recipes) is list:
        updated_recipes = []
        for recipe in recipes:
            is_favorited = await favorite_crud.get(
                user_id, recipe.id, session
            )
            is_shoplist = await shoppinglist_crud.get(
                user_id, recipe.id, session
            )
            recipe_db = RecipeDB.from_orm(recipe)
            if is_favorited is not None:
                recipe_db.is_favorited = True
            if is_shoplist is not None:
                recipe_db.is_in_shopping_cart = True
            updated_recipes.append(recipe_db)
        recipes = updated_recipes
    else:
        is_favorited = await favorite_crud.get(
            user_id, recipes.id, session
        )
        is_shoplist = await shoppinglist_crud.get(
            user_id, recipes.id, session
        )
        recipe_db = RecipeDB.from_orm(recipes)
        if is_favorited is not None:
            recipe_db.is_favorited = True
        if is_shoplist is not None:
            recipe_db.is_in_shopping_cart = True
        recipes = recipe_db
    return recipes
