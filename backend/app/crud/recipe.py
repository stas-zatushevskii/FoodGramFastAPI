from app.models.model import (
    Recipe, RecipesIngredients, RecipesTags, Favorite,
    ShoppingList, RecipesIngredients, RecipesTags, Tag,
    Ingredient
    )
from app.models.user import User
from app.crud.base import CRUDBase
from typing import Optional
from app.core.db import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class CRUDRecipe(CRUDBase):
    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id).options(
                    selectinload(self.model.tags),
                    selectinload(self.model.ingredients),
                    selectinload(self.model.author))
        )
        return db_obj.scalars().first()

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
        image = recipe_in_data['image']
        if image is not None:
            formated_image = await self.save_image(recipe_in_data['image'])
            recipe_in_data['image'] = formated_image
        if user is not None:
            recipe_in_data['author_id'] = user.id
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
                recipe_id=db_obj.id,
                amount=ingredient_amount
            )
            await session.execute(db_ingredient_obj)

        # добовление тегов
        for tag in tags:
            db_tag_obj = RecipesTags.insert().values(
                tag_id=tag,
                recipe_id=db_obj.id,
            )
            await session.execute(db_tag_obj)

        await session.commit()
        recipe = await session.execute(select(self.model).options(
                    selectinload(self.model.tags),
                    selectinload(self.model.ingredients),
                    selectinload(self.model.author)
                ).where(self.model.id == db_obj.id))
        return recipe.scalars().first()

    async def get_paginated_recipes(
            self,
            session: AsyncSession,
            start: int,
            limit: int,
    ):
        db_objs = await session.execute(
            select(self.model)
            .offset(start)
            .limit(limit)
        )
        return db_objs.scalars().all()

    '''
            stmt = select(A)
                    .join(AB)
                    .join(B)
                    .where(B.id == b_id)
    '''
    async def get_recipes_by_relation(
            self,
            session: AsyncSession,
            user_id: int,
            related_model
    ):
        recipes = await session.execute(
            select(self.model)
            .join(related_model)
            .where(related_model.user == user_id)
        )
        return recipes.scalar()

    async def get_recipes_by_tag(
            self,
            session: AsyncSession,
            tags: list[str]
    ):
        recipes = await session.execute(
            select(self.model)
            .join(RecipesTags)
            .join(Tag)
            .filter(Tag.slug.in_(tags))
        )
        return recipes

    async def get_by_author(
            self,
            session: AsyncSession,
            author_id: int
    ):
        recipes = await session.execute(
            select(self.model).where(
                self.model.author_id == author_id
            )
        )
        return recipes.scalars().all()

    async def get_recipes_with_param(
            self,
            session: AsyncSession,
            start: int,
            limit: int,
            author_id: Optional[int],
            user_id: Optional[int],
            tags: list[str],
            is_favorited: Optional[bool],
            is_in_shopping_cart: Optional[bool],
    ):
        recipes = select(self.model).options(
            selectinload(self.model.tags),
            selectinload(self.model.ingredients),
            selectinload(self.model.author)
            )
        if author_id:
            recipes = recipes.where(
                    self.model.author_id == author_id
                )

        if tags:
            recipes = recipes.join(
                RecipesTags
            ).join(Tag).filter(Tag.slug.in_(tags))

        if is_favorited:
            recipes = recipes.join(Favorite).where(
                Favorite.user == user_id)

        if is_in_shopping_cart:
            recipes = recipes.join(ShoppingList).where(
                ShoppingList.user == user_id)

        result = await session.execute(
            recipes.offset(start).limit(limit).distinct()
        )
        return result.scalars().all()


recipe_crud = CRUDRecipe(Recipe)