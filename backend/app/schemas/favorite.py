from pydantic import BaseModel
from typing import Optional


class FavoriteBase(BaseModel):
    id: Optional[int]
    recipe: int
    user: int

    class Config:
        orm_mode = True
