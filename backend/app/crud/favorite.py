from sqlalchemy import and_, select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models import Favorite, Recipe


class CRUDFavorite(CRUDBase):
    async def create(self, user_id: int, recipe_id: int, session: AsyncSession):
        data = {"user": user_id, "recipe": recipe_id}
        db_obj = self.model(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        recipe = await session.execute(select(Recipe).where(Recipe.id == recipe_id))
        return recipe.scalars().first()

    async def get(self, user_id: int, recipe_id: int, session: AsyncSession):
        result = await session.execute(
            select(self.model).where(
                and_(self.model.user == user_id, self.model.recipe == recipe_id)
            )
        )
        return result.scalars().first()


favorite_crud = CRUDFavorite(Favorite)
