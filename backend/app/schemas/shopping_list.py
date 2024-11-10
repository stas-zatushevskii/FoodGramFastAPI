from typing import Optional

from pydantic import BaseModel


class Shopping_listBase(BaseModel):
    id: Optional[int]
    recipe: int
    user: int

    class Config:
        orm_mode = True
