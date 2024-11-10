from typing import Optional

from pydantic import BaseModel


class Tag(BaseModel):
    id: Optional[int]
    name: str
    color: str
    slug: str

    class Config:
        orm_mode = True