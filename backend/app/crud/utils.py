from typing import Union

from sqlalchemy import and_, select

from app.core.db import AsyncSession
from app.crud.favorite import favorite_crud
from app.crud.recipe import recipe_crud
from app.crud.shopping_list import shoppinglist_crud
from app.crud.subscription import follow_crud
from app.models import RecipesIngredients, User
from app.schemas.ingredient import Ingredient
from app.schemas.recipe import RecipeDB
from app.schemas.user import UserRecipes


async def update_recipes_with_details(
        recipes,
        user_id: int,
        session: AsyncSession
):
    if type(recipes) is list:
        updated_recipes = []
        for recipe in recipes:
            recipe_db = RecipeDB.from_orm(recipe)
            recipe_db.ingredients = []
            # favorite и shopping_list

            is_favorited = await favorite_crud.get(
                user_id, recipe.id, session
            )
            is_shoplist = await shoppinglist_crud.get(
                user_id, recipe.id, session
            )

            if is_favorited is not None:
                recipe_db.is_favorited = True
            if is_shoplist is not None:
                recipe_db.is_in_shopping_cart = True

            # ингредиенты
            for ingredient in recipe.ingredients:
                ingredient_db = Ingredient.from_orm(ingredient)
                amount = await session.execute(
                    select(RecipesIngredients.amount).
                    where(and_(
                        RecipesIngredients.recipe_id == recipe.id,
                        RecipesIngredients.ingredient_id == ingredient.id)
                    ))
                ingredient_db.amount = amount.scalars().first()
                recipe_db.ingredients.append(ingredient_db)
            updated_recipes.append(recipe_db)
        recipes = updated_recipes
    else:
        recipe_db = RecipeDB.from_orm(recipes)
        recipe_db.ingredients = []
        # favorite и shopping_list

        is_favorited = await favorite_crud.get(
            user_id, recipes.id, session
        )
        is_shoplist = await shoppinglist_crud.get(
            user_id, recipes.id, session
        )

        if is_favorited is not None:
            recipe_db.is_favorited = True
        if is_shoplist is not None:
            recipe_db.is_in_shopping_cart = True

        # ингредиенты
        for ingredient in recipes.ingredients:
            ingredient_db = Ingredient.from_orm(ingredient)
            amount = await session.execute(
                select(RecipesIngredients.amount).
                where(and_(
                    RecipesIngredients.recipe_id == recipes.id,
                    RecipesIngredients.ingredient_id == ingredient.id)
                ))
            ingredient_db.amount = amount.scalars().first()
            recipe_db.ingredients.append(ingredient_db)
        recipes = recipe_db
    return recipes


async def get_ingredient(
        recipes,
        session: AsyncSession
):
    if type(recipes) is list:
        updated_ingredients = []
        for recipe in recipes:
            for ingredient in recipe.ingredients:
                ingredient_db = Ingredient.from_orm(ingredient)
                amount = await session.execute(
                    select(RecipesIngredients.amount).
                    where(and_(
                        RecipesIngredients.recipe_id == recipe.id,
                        RecipesIngredients.ingredient_id == ingredient.id)
                    ))
                ingredient_db.amount = amount.scalars().first()
                if ingredient_db not in updated_ingredients:
                    updated_ingredients.append(ingredient_db)
        ingredient = updated_ingredients
    else:
        for ingredient in recipes.ingredients:
            ingredient_db = Ingredient.from_orm(ingredient)
            amount = await session.execute(
                select(RecipesIngredients.amount).
                where(and_(
                    RecipesIngredients.recipe_id == recipe.id,
                    RecipesIngredients.ingredient_id == ingredient.id)
                ))
            ingredient_db.amount = amount.scalars().first()
        ingredient = ingredient_db
    return ingredient


async def get_follows_with_param(
        user_id: int,
        recipes_limit: int,
        authors: Union[list[User], User],
        session: AsyncSession

):
    results = []
    if type(authors) is list:
        for author in authors:
            author_db = UserRecipes.from_orm(author)
            author_db.is_subscribed = await follow_crud.get_is_subscribed(
                user_id=user_id, author_id=author.id, session=session
            )
            author_db.recipes_made = await recipe_crud.get_by_author(
                author_id=author.id, session=session, limit=recipes_limit
            )
            author_db.recipes_count = await recipe_crud.count_recipes(
                session=session, author_id=author.id
                )
            results.append(author_db)
        return results
    else:
        author_db = UserRecipes.from_orm(authors)
        author_db.is_subscribed = await follow_crud.get_is_subscribed(
            user_id=user_id, author_id=authors.id, session=session
        )
        author_db.recipes_made = await recipe_crud.get_by_author(
            author_id=authors.id, session=session, limit=recipes_limit
        )
        author_db.recipes_count = await recipe_crud.count_recipes(
            session=session, author_id=authors.id
            )
        return author_db
