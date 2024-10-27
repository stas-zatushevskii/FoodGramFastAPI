from app.crud.base import CRUDBase
from app.models import Ingredient
from app.core.db import AsyncSession
from sqlalchemy import select


class CRUDIngredient(CRUDBase):
    async def get_ingredient_by_name(
            self,
            ingredient_name: str,
            session: AsyncSession
    ):
        ingredient = await session.execute(
            select(self.model).where(Ingredient.name.like(f'{ingredient_name}%'))
        )
        return ingredient.scalars().all()
ingredient_crud = CRUDIngredient(Ingredient)