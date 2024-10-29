from pydantic import BaseModel
from typing import Optional


class Shopping_listBase(BaseModel):
    id: Optional[int]
    recipe: int
    user: int

    class Config:
        orm_mode = True
