from sqlalchemy import and_, select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models import RecipesTags, Tag


class CRUDTag(CRUDBase):
    async def add_tag(self, tag_id: int, recipe_id: int, session: AsyncSession):
        data = {
            "recipe_id": recipe_id,
            "tag_id": tag_id,
        }
        db_obj = RecipesTags(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete_from_recipe(
        self, tag_id: int, recipe_id: int, session: AsyncSession
    ):
        tag = await session.execute(
            select(RecipesTags).where(
                and_(RecipesTags.tag_id == tag_id, RecipesTags.recipe_id == recipe_id)
            )
        )
        await session.delete(tag.scalar_one_or_none())
        await session.commit()
        return tag

    async def tags_update(
        self, tags_delete: set, tags_update: set, recipe_id: int, session: AsyncSession
    ):
        # удаление
        for tag_id in tags_delete:
            await tag_crud.delete_from_recipe(tag_id, recipe_id, session)
        # создание
        for tag_obj in tags_update:
            await tag_crud.add_tag(tag_obj, recipe_id, session)


tag_crud = CRUDTag(Tag)
