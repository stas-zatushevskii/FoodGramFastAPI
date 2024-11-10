from typing import Optional, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_follow_exist
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.recipe import recipe_crud
from app.crud.subscription import follow_crud
from app.crud.utils import get_follows_with_param
from app.models.user import User

router = APIRouter()


@router.get(
    "/users/subscriptions/"
)
async def get_follows(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
    page: int = 1,
    limit: int = 6,
    recipes_limit: Optional[int] = 6
):
    start = (page - 1) * limit
    authors_id = await follow_crud.get_follows(user.id, session, start, limit)
    users_db = await get_follows_with_param(
        user_id=user.id,
        authors=authors_id,
        recipes_limit=recipes_limit,
        session=session)
    count_follows = await follow_crud.count_follows(user.id, session)
    next_page = f'/api/users/subscriptions/?page={page+1}'
    if page != 1:
        previous_page = f'/api/users/subscriptions/?page={page-1}'
    else:
        previous_page = f'/api/users/subscriptions//?page={page}'
    return {
        "count": count_follows,
        "next": next_page,
        "pervious": previous_page,
        "results": users_db,
    }


# поменять return
@router.post(
    "/users/{author_id}/subscribe/"
)
async def follow(
    author_id: int,
    recipes_limit: Optional[int] = 6,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    await check_follow_exist(user.id, author_id, session, exist=False)
    await follow_crud.create(user.id, author_id, session)
    author = await follow_crud.get_user(author_id, session)
    user_db = await get_follows_with_param(
        user_id=user.id,
        authors=author,
        recipes_limit=recipes_limit,
        session=session)
    return user_db


@router.delete(
    "/users/{author_id}/subscribe/"
)
async def unfollow(
    recipe_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    await follow_crud.delete(user.id, author_id, session)
    return {"message": "вы отписались от пользователя"}
