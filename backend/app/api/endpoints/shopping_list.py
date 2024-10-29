# api/recipes/{id}/shopping_cart/

from app.core.db import get_async_session
from fastapi import APIRouter, Depends
from app.schemas.recipe import RecipeGet
from app.schemas.shopping_list import Shopping_listBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.validators import check_shopping_list_exist
from app.core.user import current_user
from app.models.user import User
from app.crud.shopping_list import shoppinglist_crud


router = APIRouter()


@router.get(
        "/shopping_carts/",
        response_model=list[Shopping_listBase],
        response_model_exclude_none=True
)
async def get_shopping_list(
    session: AsyncSession = Depends(get_async_session)
):
    shopping_list = await shoppinglist_crud.get_multi(session)
    return shopping_list


@router.post(
        "/recipes/{recipe_id}/shopping_cart/",
        response_model=RecipeGet,
        response_model_exclude_none=True
)
async def add_in_shoplist(
    recipe_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    await check_shopping_list_exist(user.id, recipe_id, session, exist=False)
    result = await shoppinglist_crud.create(user.id, recipe_id, session)
    return result


@router.delete(
        "/recipes/{recipe_id}/shopping_cart/",
        response_model_exclude_none=True
)
async def delete_shoplist(
    recipe_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    shopping_list = await check_shopping_list_exist(
        recipe_id, user.id, session, exist=True,
    )
    await shoppinglist_crud.delete(shopping_list, session)
    return {'message': 'Рецепт успешно удален из списка!'}
