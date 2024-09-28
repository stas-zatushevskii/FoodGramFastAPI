from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.schemas.recipe import RecipeList
from app.crud.base import CRUDBase
from app.models.model import Recipe


router = APIRouter()
crud = CRUDBase(Recipe)

@router.get("/",
            response_model=list[RecipeList],
            response_model_exclude_none=True
)
async def get_recipes(
        session: AsyncSession = Depends(get_async_session),
):
    all_recipes = await crud.get_multi(session)
    return all_recipes