from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.schemas.recipe import RecipeList, RecipeDB, RecipeCreate
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

@router.post(
    '/',
    response_model=RecipeDB,
    response_model_exclude_none=True,
    # Добавьте вызов зависимости при обработке запроса.
)
async def create_new_recipe(
        recipe: RecipeCreate,
        session: AsyncSession = Depends(get_async_session),
):
    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    new_recipe = await crud.create(recipe, session)
    return new_recipe