from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.favorite import favorite_crud
from app.crud.recipe import recipe_crud
from app.crud.shopping_list import shoppinglist_crud
from app.crud.subscription import follow_crud
from app.models import Favorite, Recipe, ShoppingList
from app.models.user import followers


async def check_shopping_list_exist(
    user_id: int, recipe_id: int, session: AsyncSession, exist: bool
) -> ShoppingList:
    list = await shoppinglist_crud.get(user_id, recipe_id, session)
    # если лист должен существовать для коректной проверки
    if exist:
        if list is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Рецепт не найден!"
            )
        return list
    # если лист не должен существовать для коректной проверки
    else:
        if list is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Рецепт уже есть в списке покупок",
            )


async def check_favorite_exist(
    user_id: int, recipe_id: int, session: AsyncSession, exist: bool
) -> Favorite:
    favorite = await favorite_crud.get(user_id, recipe_id, session)
    # если лист должен существовать для коректной проверки
    if exist:
        if favorite is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Рецепт не найден!"
            )
        return favorite

    # если избранный не должен существовать для коректной проверки
    else:
        if favorite is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Рецепт уже есть в списке избранных",
            )


async def check_follow_exist(
    user_id: int, author_id: int, session: AsyncSession, exist: bool
):
    follow = await follow_crud.get_follow(user_id, author_id, session)
    # если подписка должна существовать для коректной проверки
    if exist:
        if follow is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Объект не найден!"
            )
        return follow

    # если подписки не должен существовать для коректной проверки
    else:
        if follow is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Вы уже подписанны на данного пользователя",
            )


async def check_recipe_exist(
    recipe_id: int,
    author_id,
    session: AsyncSession,
) -> Recipe:
    recipe = await recipe_crud.get(recipe_id, session)
    # если лист должен существовать для коректной проверки
    if recipe is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Рецепт не найден!"
        )
    if recipe.author.id != author_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Вы не являетесь автором рецепта!",
        )
    return recipe
