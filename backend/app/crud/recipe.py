from app.models.model import Recipe, RecipesIngredients, RecipesTags
from app.models.user import User
from app.crud.base import CRUDBase
from typing import Optional
from app.core.db import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class CRUDRecipe(CRUDBase):
    async def count_recipes(
            self,
            session: AsyncSession
    ):
        count = await session.execute(
            select(func.count(self.model.id))
        )
        return count.scalar()

    async def create(
            self,
            recipe_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        # получаем tags, ingredients
        ingredients = recipe_in.ingredients
        tags = recipe_in.tags
        recipe_in.ingredients, recipe_in.tags = [], []

        # создаем recipe
        recipe_in_data = recipe_in.dict()
        if user is not None:
            recipe_in_data['author'] = user.id
        db_obj = self.model(**recipe_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        # добовление ингердиентов
        for ingredient in ingredients:
            ingredient_data = ingredient.dict()
            ingredient_id = ingredient_data['id']
            ingredient_amount = ingredient_data['amount']
            db_ingredient_obj = RecipesIngredients.insert().values(
                ingredient_id=ingredient_id,
                recipe_id = db_obj.id,
                amount=ingredient_amount
            )
            await session.execute(db_ingredient_obj)

        # добовление тегов
        for tag in tags:
            db_tag_obj = RecipesTags.insert().values(
                tag_id=tag,
                recipe_id = db_obj.id,
            )
            await session.execute(db_tag_obj)

        await session.commit()
        return db_obj

    async def get_paginated_recipes(
            self,
            session: AsyncSession,
            start: int,
            limit: int,
    ):


        db_objs = await session.execute(
            #select(self.model).offset(start).limit(limit))
            select(self.model).offset(start).limit(limit).options(selectinload(self.model.tags)))
        return db_objs.scalars().all()

recipe_crud = CRUDRecipe(Recipe)

'''            author: User ,
            is_favorited: int,
            is_in_shopping_cart: int,
            tags: Optional[list] = None,'''