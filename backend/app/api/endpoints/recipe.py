from typing import Optional, Union

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_recipe_exist
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.recipe import recipe_crud
from app.crud.utils import update_recipes_with_details
from app.models.user import User
from app.schemas.recipe import RecipeCreate, RecipeDB, RecipeList, RecipeUpdate

router = APIRouter()


@router.get(
    "/recipes/",
    response_model=RecipeList,
    response_model_exclude_none=True,
)
async def get_recipes(
    session: AsyncSession = Depends(get_async_session),
    page: int = 1,
    limit: int = 6,
    is_favorited: Optional[bool] = False,
    is_in_shopping_cart: Optional[bool] = False,
    author_id: Optional[int] = None,
    tags: Optional[list[str]] = Query(None),
    user: User = Depends(current_user),
):
    start = (page - 1) * limit
    user_id = user.id
    all_recipes = await recipe_crud.get_recipes_with_param(
        session,
        start,
        limit,
        author_id,
        user_id,
        tags,
        is_favorited,
        is_in_shopping_cart,
    )
    recipes_db = await update_recipes_with_details(all_recipes, user.id, session)
    count_recipes = await recipe_crud.count_recipes(
        session,
        user_id=user.id,
        is_shopping_card=is_in_shopping_cart,
        favorite=is_favorited,
    )
    next_page = f"/api/recipes/?page={page+1}"
    if page != 1:
        previous_page = f"/api/recipes/?page={page-1}"
    else:
        previous_page = f"/api/recipes/?page={page}"
    return {
        "count": count_recipes,
        "next": next_page,
        "pervious": previous_page,
        "results": recipes_db,
    }


@router.post(
    "/recipes/",
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
    "/recipes",
    response_model=Union[RecipeDB, list[RecipeDB]],
    response_model_exclude_none=True,
)
async def get_recipe_by_author(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    author_id = user.id
    return await recipe_crud.get_by_author(session, author_id)


@router.get(
    "/recipes/{id}/",
    response_model=RecipeDB,
    response_model_exclude_none=True,
)
async def get_recipe(
    id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    recipe = await recipe_crud.get(id, session)
    recipe_db = await update_recipes_with_details(recipe, user.id, session)
    return recipe_db


@router.patch(
    "/recipes/{recipe_id}/", response_model=RecipeDB, response_model_exclude_none=True
)
async def update_recipe(
    recipe_id: int,
    recipe_in: RecipeUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    recipe_db = await recipe_crud.get(recipe_id, session)
    recipe_update = await recipe_crud.update(recipe_db, recipe_in, session)
    recipe_with_detail = await update_recipes_with_details(
        recipe_update, user.id, session
    )
    return recipe_with_detail


@router.delete("/recipes/{recipe_id}/")
async def delete_recipe(
    recipe_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    reccipe = await check_recipe_exist(recipe_id, user.id, session)
    await recipe_crud.delete(reccipe, session)
    return {"message": "Рецепт успешно удален"}
