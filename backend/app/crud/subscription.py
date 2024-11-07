from app.models import User, followers
from app.core.db import AsyncSession
from sqlalchemy import select, and_, func
from app.crud.base import CRUDBase
from app.schemas.user import UserRecipes
from app.crud.recipe import recipe_crud
from typing import Optional
from sqlalchemy import delete


# написать валидатор
class CRUDFollow(CRUDBase):
    async def create(
            self,
            user_id: int,
            author_id: int,
            session: AsyncSession
    ):
        follow_in_data = {
            'author_id': author_id,
            'follower_id': user_id
        }
        await session.execute(followers.insert().values(**follow_in_data))
        await session.commit()

    async def get_user(
            self,
            user_id: int,
            session: AsyncSession
    ):
        author = await session.execute(
            select(self.model)
            .where(self.model.id == user_id)
        )
        return author.scalars().first()

    async def get_follows(
            self,
            user_id: int,
            session: AsyncSession,
            start: Optional[int] = 0,
            limit: Optional[int] = 6,
    ):
        followings = await session.execute(select(followers.c.author_id).where(
            followers.c.follower_id == user_id
        ).offset(start).limit(limit))

        authors = await session.execute(
            select(self.model)
            .where(self.model.id.in_(followings.scalars().all()))
        )
        return authors.scalars().all()

    async def count_follows(
            self,
            user_id: int,
            session: AsyncSession
    ):
        followings = await session.execute(
            select(func.count(followers.c.author_id))
            .where(followers.c.follower_id == user_id)
        )
        return followings.scalar()

    async def get_is_subscribed(
            self,
            user_id: int,
            author_id: int,
            session: AsyncSession
    ):
        is_subscribed = await session.execute(
            select(followers)
            .where(and_(
                followers.c.author_id == author_id,
                followers.c.follower_id == user_id
                )
            )
        )
        if is_subscribed.scalars().first() is not None:
            return True
        return False

    async def get_follow(
            self,
            user_id: int,
            author_id: int,
            session: AsyncSession
    ):
        follow = await session.execute(
            select(followers)
            .where(and_(
                followers.c.author_id == author_id,
                followers.c.follower_id == user_id
                )
            )
        )
        return follow.scalars().first()

    async def get_follows_with_param(
            self,
            user_id: int,
            authors: list[User],
            session: AsyncSession

    ):
        results = []
        for author in authors:
            author_db = UserRecipes.from_orm(author)
            author_db.is_subscribed = self.get_is_subscribed(
                user_id=user_id, author_id=author.id, session=session
            )
            author_db.recipes_made = recipe_crud.get_by_author(
                author_id=author.id, session=session
            )
            author_db = recipe_crud.count_recipes(
                session=session, author_id=author.id
                )
            results.append(author_db)
        return results

    async def delete(
            self,
            user_id: int,
            author_id: int,
            session: AsyncSession
    ):
        follow = delete(followers).where(
            followers.c.author_id == author_id,
            followers.c.follower_id == user_id
        )
        await session.execute(follow)
        await session.commit()


follow_crud = CRUDFollow(User)
