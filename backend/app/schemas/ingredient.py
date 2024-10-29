from typing import Optional

from pydantic import BaseModel


class Ingredient(BaseModel):
    id: int
    name: str
    measurement_unit: str
    amount: Optional[int]

    class Config:
        orm_mode = True


class IngredientInRecipe(BaseModel):
    id: int
    amount: Optional[int]

    class Config:
        orm_mode = True