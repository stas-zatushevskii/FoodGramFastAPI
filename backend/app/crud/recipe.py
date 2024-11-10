from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.crud.ingredient import ingredient_crud
from app.crud.tag import tag_crud
from app.models.model import (Favorite, Recipe, RecipesIngredients,
                              RecipesTags, ShoppingList, Tag)
from app.models.user import User
from app.schemas.recipe import RecipeCreate, RecipeUpdate


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
            session: AsyncSession,
            author_id: Optional[int] = None,
            user_id: Optional[int] = None,
            is_shopping_card: Optional[bool] = False,
            favorite: Optional[bool] = False
    ):
        if is_shopping_card is True:
            count = await session.execute(
                select(func.count(ShoppingList.id))
                .where(ShoppingList.user == user_id)
            )
            return count.scalar()
        elif favorite is True:
            count = await session.execute(
                select(func.count(Favorite.id))
                .where(Favorite.user == user_id)
            )
            return count.scalar()
        elif author_id is not None:
            count = await session.execute(
                select(func.count(self.model.id))
                .where(self.model.author_id == author_id)
            )
            return count.scalar()
        else:
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

            db_ingredient_obj = RecipesIngredients(
                ingredient_id=ingredient_id,
                recipe_id=db_obj.id,
                amount=ingredient_amount
            )
            session.add(db_ingredient_obj)

        # добовление тегов
        for tag in tags:
            db_tag_obj = RecipesTags(
                tag_id=tag,
                recipe_id=db_obj.id,
            )
            session.add(db_tag_obj)

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
            author_id: int,
            limit: Optional[int] = None
    ):
        if limit is None:
            recipes = await session.execute(
                select(self.model).where(
                    self.model.author_id == author_id
                )
            )
            return recipes.scalars().all()
        else:
            recipes = await session.execute(
                select(self.model).where(
                    self.model.author_id == author_id
                ).limit(limit)
            )
            return recipes.scalars().all()

    async def get_recipes_with_param(
            self,
            session: AsyncSession,
            start: int,
            limit: int,
            author_id: Optional[Union[int, list[int]]] = None,
            user_id: Optional[Union[int, list[int]]] = None,
            tags: Optional[list[str]] = None,
            is_favorited: Optional[bool] = None,
            is_in_shopping_cart: Optional[bool] = None,
    ):
        recipes = select(self.model).options(
            selectinload(self.model.tags),
            selectinload(self.model.ingredients),
            selectinload(self.model.author)
            )
        if author_id:
            # если author_id - list то гуд
            # если же нет то в in_ передается
            # [author_id]
            author_id = author_id if isinstance(
                author_id,
                list
            ) else [author_id]
            recipes = recipes.filter(
                    self.model.author_id.in_(author_id))

        if tags:
            recipes = recipes.join(
                RecipesTags
            ).join(Tag).filter(Tag.slug.in_(tags))

        if is_favorited:
            user_id = user_id if isinstance(
                user_id,
                list
            ) else [user_id]
            recipes = recipes.join(Favorite).filter(
                Favorite.user.in_(user_id))

        if is_in_shopping_cart:
            user_id = user_id if isinstance(
                user_id,
                list
            ) else [author_id]
            recipes = recipes.join(ShoppingList).filter(
                ShoppingList.user.in_(user_id))

        result = await session.execute(
            recipes.offset(start).limit(limit).distinct()
        )
        recipe = result.scalars().all()
        return recipe

    async def update(
            self,
            db_obj: RecipeCreate,
            in_obj: RecipeUpdate,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = in_obj.dict(exclude_unset=True)
        for field in update_data:
            if field in obj_data:
                if field == 'ingredients':
                    # ingredients_delete = []
                    # ingredients_add = []
                    # crud function to update ingredients in recipe
                    ingredients_old = [
                        ingredient['id'] for ingredient in obj_data[field]
                    ]
                    ingredients_new = [
                        ingredient['id'] for ingredient in update_data[field]
                    ]
                    ingredients_delete = set(ingredients_old) - set(
                        ingredients_new
                        )
                    ingredients_add = set(ingredients_new) - set(
                        ingredients_old
                        )
                    ingredients_add_obj = [
                        ingredient for ingredient in update_data[field] if ingredient['id'] in ingredients_add
                        ]
                    if ingredients_add_obj or ingredients_delete:
                        await ingredient_crud.ingredints_update(
                            ingredients_delete,
                            ingredients_add_obj,
                            db_obj.id,
                            session
                        )
                    continue
                elif field == 'tags':
                    # crud function to update tags in recipe
                    tags_old = [
                        tag['id'] for tag in obj_data[field]
                    ]
                    tags_new = [
                        tag for tag in update_data[field]
                    ]
                    tags_delete = set(tags_old) - set(
                        tags_new
                    )
                    tags_add = set(tags_new) - set(
                        tags_old
                    )
                    if tags_add or tags_delete:
                        await tag_crud.tags_update(
                            tags_delete,
                            tags_add,
                            db_obj.id,
                            session
                        )
                    continue
                elif field == 'image':
                    update_data[field] = await recipe_crud.save_image(
                        update_data[field]
                    )
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


recipe_crud = CRUDRecipe(Recipe)
