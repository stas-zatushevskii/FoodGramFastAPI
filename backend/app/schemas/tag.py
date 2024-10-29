from pydantic import BaseModel
from typing import Optional


class Tag(BaseModel):
    id: Optional[int]
    name: str
    color: str
    slug: str

    class Config:
        orm_mode = True