from typing import Optional

from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    name: str
    measurement_unit: str
    amount: int
