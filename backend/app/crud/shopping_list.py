from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models import Recipe, ShoppingList


class CRUDShoppingList(CRUDBase):
    async def create(
            self,
            user_id: int,
            recipe_id: int,
            session: AsyncSession
    ):
        try:
            data = {
                "user": user_id,
                "recipe": recipe_id
            }
            db_obj = self.model(**data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            recipe = await session.execute(select(Recipe).where(
                Recipe.id == recipe_id)
            )
            return recipe.scalars().first()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при создании: {e}")
            raise

    async def get_lists(
            self,
            user_id: int,
            session: AsyncSession
    ):
        lists = await session.execute(
            select(self.model)
            .where(
                self.model.user == user_id))
        return lists.scalars().all()

    async def get_recipes(
            self,
            user_id,
            session: AsyncSession
    ):
        recipes_id_subquery = await session.execute(
            select(self.model.recipe)
            .where(self.model.user == user_id)
        )
        recipes = await session.execute(select(Recipe).options(
            selectinload(Recipe.ingredients)).where(
            Recipe.id.in_(recipes_id_subquery.scalars().all())
        ))
        return recipes.scalars().all()

    async def get(
            self,
            user_id: int,
            recipe_id: int,
            session: AsyncSession
    ):
        result = await session.execute(
            select(self.model)
            .where(
                and_(
                    self.model.user == user_id,
                    self.model.recipe == recipe_id))
        )
        result = result.scalars().first()
        return result


shoppinglist_crud = CRUDShoppingList(ShoppingList)
