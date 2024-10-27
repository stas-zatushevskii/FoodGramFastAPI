from cgitb import reset

from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.schemas.recipe import RecipeList, RecipeDB, RecipeCreate
from app.crud.recipe import recipe_crud
from app.core.user import current_user

from app.models.user import User
from typing import Optional


router = APIRouter()

@router.get("/recipes/",
            response_model=RecipeList,
            response_model_exclude_none=True
)
async def get_recipes(
        session: AsyncSession = Depends(get_async_session),
        page: int = 1,
        limit: int = 6,
        is_favorited: Optional[bool] = False,
        is_in_shopping_cart: Optional[bool] = False,
        author: Optional[int] = None,
        tag: Optional[int] = None,
):
    '''
    Подгрузить  tags (RecipesTags) и ingredients (RecipesIngredients)
    Подгрузить is_favorite(??current_user.id == Favorite.user.id -> Favorite.recipe.id == recipe.id)
    Подгрузить is_in_shopping_cart(??current_user.id == ShoppingList.user.id -> ShoppingList.recipe.id == recipe.id)
    '''
    start = (page - 1) * limit
    all_recipes = await recipe_crud.get_paginated_recipes(session, start, limit)
    count_recipes = await recipe_crud.count_recipes(session)
    next_page = f'api/recipes/?page={page}'
    if page != 1:
        previous_page = f'api/recipes/?page={page-1}'
    else:
        previous_page = f'api/recipes/?page={page}'
    return {
        "count": count_recipes,
        "next": next_page,
        "pervious": previous_page,
        "results": all_recipes,
    }


@router.post(
    '/recipe/',
    response_model=RecipeDB,
    response_model_exclude_none=True,
)
async def create_new_recipe(
        recipe: RecipeCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_recipe = await recipe_crud.create(recipe, session, user)
    return new_recipe

@router.get(
    '/recipes/{id}',
    response_model=list[RecipeDB],
    response_model_exclude_none=True,
)