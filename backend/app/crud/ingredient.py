from sqlalchemy import and_, select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models import Ingredient, RecipesIngredients


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

    async def add_ingredient(
            self,
            ingredient_id: int,
            recipe_id: int,
            amount: int,
            session: AsyncSession
    ):
        data = {
            'recipe_id': recipe_id,
            'ingredient_id': ingredient_id,
            'amount': amount
        }
        db_obj = RecipesIngredients(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

    async def delete_from_recipe(
            self,
            ingredient_id: int,
            recipe_id: int,
            session: AsyncSession
    ):
        ingredient = await session.execute(
            select(RecipesIngredients)
            .where(and_(
                RecipesIngredients.ingredient_id == ingredient_id,
                RecipesIngredients.recipe_id == recipe_id
            ))
        )
        await session.delete(ingredient.scalar_one_or_none())
        await session.commit()

    async def ingredints_update(
            self,
            ingredients_delete: set,
            ingredients_update: dict,
            recipe_id: int,
            session: AsyncSession
    ):
        # удаление
        for ingredient_id in ingredients_delete:
            await self.delete_from_recipe(
                ingredient_id, recipe_id, session)
        # создание
        for ingredient_obj in ingredients_update:
            await self.add_ingredient(
                ingredient_obj['id'],
                recipe_id,
                ingredient_obj['amount'],
                session
            )


ingredient_crud = CRUDIngredient(Ingredient)