from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserInRecipe
from fastapi import APIRouter, Depends
from app.models.user import User

from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user_crud

router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/users',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)

current_user = fastapi_users.current_user()


@router.get(
    "/users/{user_id}/",
    response_model=UserInRecipe,
    response_model_exclude=['recipes_count']
)
async def get(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get(user_id, session)
    return user
