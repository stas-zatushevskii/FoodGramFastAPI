# app/api/routers.py
from fastapi import APIRouter

from app.api.endpoints import (
    data_router,
    favorite_router,
    ingredient_router,
    recipe_router,
    shopping_list_router,
    subscriptions_router,
    tag_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(subscriptions_router, tags=["subscriptions"])
main_router.include_router(user_router)
main_router.include_router(data_router, tags=["data"])
main_router.include_router(tag_router, tags=["tags"])
main_router.include_router(ingredient_router, tags=["ingredients"])
main_router.include_router(shopping_list_router, tags=["shopping_list"])
main_router.include_router(favorite_router, tags=["favorite"])
main_router.include_router(recipe_router, tags=["recipes"])
