from app.core.db import get_async_session
from fastapi import APIRouter, Depends
from app.schemas.recipe import RecipeGet
from app.schemas.favorite import FavoriteBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.validators import check_favorite_exist
from app.core.user import current_user
from app.models.user import User
from app.crud.favorite import favorite_crud


router = APIRouter()


@router.get(
        "/favorites/",
        response_model=list[FavoriteBase],
        response_model_exclude_none=True
)
async def get_favorite(
    session: AsyncSession = Depends(get_async_session)
):
    favorite = await favorite_crud.get_multi(session)
    return favorite


@router.post(
        "/recipes/{recipe_id}/favorite/",
        response_model=RecipeGet,
        response_model_exclude_none=True
)
async def add_in_favorite(
    recipe_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    await check_favorite_exist(user.id, recipe_id, session, exist=False)
    result = await favorite_crud.create(user.id, recipe_id, session)
    return result


@router.delete(
        "/recipes/{recipe_id}/favorite/",
        response_model_exclude_none=True
)
async def delete_favorite(
    recipe_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    favorite = await check_favorite_exist(
        user.id, recipe_id, session, exist=True
    )
    await favorite_crud.delete(favorite, session)
    return {'message': 'Рецепт успешно удален из избранных!'}
