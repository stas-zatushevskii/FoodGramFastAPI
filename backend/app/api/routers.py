# app/api/routers.py
from fastapi import APIRouter

from app.api.endpoints import user_router, data_router, recipe_router, tag_router, ingredient_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(data_router, tags=['data'])
main_router.include_router(tag_router, tags=['tags'])
main_router.include_router(recipe_router, tags=['recipes'])
main_router.include_router(ingredient_router, tags=['ingredients'])