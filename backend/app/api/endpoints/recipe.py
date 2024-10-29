from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.schemas.recipe import RecipeList, RecipeDB, RecipeCreate
from app.crud.recipe import recipe_crud
from app.core.user import current_user
from fastapi import Query
from app.crud.utils import set_favorite_shoplist


from app.models.user import User
from app.models import Favorite, ShoppingList
from typing import Optional, Union


router = APIRouter()


@router.get(
        "/recipes/",
        response_model=RecipeList,
        response_model_exclude_none=True,
)
async def get_recipes(
        session: AsyncSession = Depends(get_async_session),
        page: int = 1,
        limit: int = 6,
        is_favorited: Optional[bool] = False,
        is_in_shopping_cart: Optional[bool] = False,
        author_id: Optional[int] = None,
        tags: Optional[list[str]] = Query(None),
        user: User = Depends(current_user),
):
    start = (page - 1) * limit
    user_id = user.id
    all_recipes = await recipe_crud.get_recipes_with_param(
        session,
        start,
        limit,
        author_id,
        user_id,
        tags,
        is_favorited,
        is_in_shopping_cart
    )
    recipes_db = await set_favorite_shoplist(all_recipes, user.id, session)
    count_recipes = await recipe_crud.count_recipes(session)
    next_page = f'/api/recipes/?page={page+1}'
    if page != 1:
        previous_page = f'/api/recipes/?page={page-1}'
    else:
        previous_page = f'/api/recipes/?page={page}'
    return {
        "count": count_recipes,
        "next": next_page,
        "pervious": previous_page,
        "results": recipes_db,
    }


@router.post(
    '/recipes/',
    response_model=RecipeDB,
    response_model_exclude_none=True,
)
async def create_new_recipe(
        recipe: RecipeCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_recipe = await recipe_crud.create(recipe, session, user)
    return new_recipe


@router.get(
    '/recipes',
    response_model=Union[RecipeDB, list[RecipeDB]],
    response_model_exclude_none=True,
)
async def get_recipe_by_author(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    author_id = user.id
    return await recipe_crud.get_by_author(session, author_id)


@router.get(
    '/recipes/{id}/',
    response_model=RecipeDB,
    response_model_exclude_none=True,
)
async def get_recipe(
        id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    recipe = await recipe_crud.get(id, session)
    recipe_db = await set_favorite_shoplist(recipe, user.id, session)
    return recipe_db
