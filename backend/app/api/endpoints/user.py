from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserInRecipe, UsreChangePassword
from fastapi import APIRouter, Depends
from app.models.user import User

from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user_crud
from app.core.user import current_user, get_user_db
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.password import PasswordHelper

router = APIRouter()
password_helper = PasswordHelper()

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


@router.post(
    '/users/set_password'
)
async def change_password(
    data: UsreChangePassword,
    current_user: User = Depends(current_user),
    db_user: SQLAlchemyUserDatabase = Depends(get_user_db)
):
    is_valid = password_helper.verify_and_update(
        data.current_password, current_user.hashed_password
    )[0]
    if is_valid is False:
        raise HTTPException(status_code=400, detail="Неверный пароль")
    hashed_new_password = password_helper.hash(data.new_password)
    await db_user.update(
        current_user,
        {'hashed_password': hashed_new_password}
    )
    return {"message": "Пароль успешно изменен"}
