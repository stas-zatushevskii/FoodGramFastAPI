# app/api/routers.py
from fastapi import APIRouter

from app.api.endpoints import user_router, data_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(data_router, tags=['data'])