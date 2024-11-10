from typing import Optional

from pydantic import BaseModel


class FavoriteBase(BaseModel):
    id: Optional[int]
    recipe: int
    user: int

    class Config:
        orm_mode = True
