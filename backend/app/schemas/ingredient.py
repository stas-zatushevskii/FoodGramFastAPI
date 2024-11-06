from typing import Optional

from pydantic import BaseModel


class Ingredient(BaseModel):
    id: Optional[int]
    name: str
    measurement_unit: str
    amount: Optional[int]

    class Config:
        orm_mode = True


class IngredientInRecipe(BaseModel):
    id: Optional[int]
    amount: Optional[int]

    class Config:
        orm_mode = True
