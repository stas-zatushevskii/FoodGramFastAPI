from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.schemas.ingredient import Ingredient
from app.crud.ingredient import ingredient_crud

from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get('/ingredients/',
             response_model=list[Ingredient],
             response_model_exclude_none=True)
async def get_ingredients(
        session: AsyncSession = Depends(get_async_session),
        name: Optional[str] = Query(None)):
    if name is not None:
        all_ingredients = await ingredient_crud.get_ingredient_by_name(name, session)
    else:
        all_ingredients = await ingredient_crud.get_multi(session)
    return all_ingredients


@router.get('/ingredients/{id}/',
             response_model=Ingredient,
             response_model_exclude_none=True)
async def get_ingredient(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    ingredient = await ingredient_crud.get(id, session)
    return ingredient
