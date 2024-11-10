import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import Ingredient

# session: AsyncSession = Depends(get_async_session),
#  [{"name": "абрикосовое варенье", "measurement_unit": "г"}]

router = APIRouter()


async def load_data(file_path: str, session: AsyncSession = Depends(get_async_session)):
    try:
        # Чтение JSON файла из указанного пути
        with open(file_path, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise HTTPException(status_code=400, detail=f"Error loading file: {str(e)}")

    for ingredient in data:
        name = ingredient["name"]
        measurement_unit = ingredient["measurement_unit"]
        ingredient = Ingredient(name=name, measurement_unit=measurement_unit)
        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)

    return {"message": "Data loaded successfully"}


@router.post("/load-from-file")
async def load_from_file(db: AsyncSession = Depends(get_async_session)):
    file_path = "data/ingredients.json"
    return await load_data(file_path, db)
