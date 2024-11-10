# api/recipes/{id}/shopping_cart/

from io import BytesIO
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_shopping_list_exist
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.shopping_list import shoppinglist_crud
from app.crud.utils import get_ingredient
from app.models.user import User
from app.schemas.recipe import RecipeGet
from app.schemas.shopping_list import Shopping_listBase

router = APIRouter()


@router.get(
    "/recipes/shopping_carts/download_shopping_cart/",
)
async def get_ingredients(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    recipes = await shoppinglist_crud.get_recipes(user.id, session)
    ingredients = await get_ingredient(recipes, session)
    file_stream = BytesIO()
    for ingredient in ingredients:
        # Пишем текст в бинарный поток
        file_stream.write(
            f"{ingredient.name} - {ingredient.amount} {ingredient.measurement_unit}\n".encode(
                "utf-8"
            )
        )

    # Возвращаем курсор в начало потока для чтения
    file_stream.seek(0)

    # Возвращаем как StreamingResponse с указанием бинарного типа
    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": 'attachment; filename="list.txt"'},
    )


@router.get(
    "/shopping_carts/",
    response_model=list[Shopping_listBase],
    response_model_exclude_none=True,
)
async def get_shopping_list(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    shopping_list = await shoppinglist_crud.get_lists(user.id, session)

    return shopping_list


@router.post(
    "/recipes/{recipe_id}/shopping_cart/",
    response_model=RecipeGet,
    response_model_exclude_none=True,
)
async def add_in_shoplist(
    recipe_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await check_shopping_list_exist(user.id, recipe_id, session, exist=False)
    result = await shoppinglist_crud.create(user.id, recipe_id, session)
    return result


@router.delete("/recipes/{recipe_id}/shopping_cart/", response_model_exclude_none=True)
async def delete_shoplist(
    recipe_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    shopping_list = await check_shopping_list_exist(
        user.id,
        recipe_id,
        session,
        exist=True,
    )
    await shoppinglist_crud.delete(shopping_list, session)
    return {"message": "Рецепт успешно удален из списка!"}
