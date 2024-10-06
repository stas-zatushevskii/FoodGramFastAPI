from typing import Optional

from pydantic import BaseModel, Field, FilePath
from datetime import datetime
from .ingredient import Ingredient
from .user import UserGet


class RecipeBase(BaseModel):
    image: str
    name: str
    description: str
    cooking_time: datetime


class RecipeCreate(RecipeBase):
    ingredients: Optional[list[Ingredient]]
    tags: Optional[list[int]]


class RecipeUpdate(RecipeBase):
    ingredients: list[Ingredient]
    tags: list[int]


class RecipeList(RecipeBase):
    page: int
    limit: int
    is_favorite: bool
    is_in_shopping_cart: bool
    author: int

    class Config:
        orm_mode = True


class RecipeGet(RecipeBase):
    id: int
    is_favorite: bool
    is_in_shopping_cart: bool
    author: UserGet

    class Config:
        orm_mode = True

class RecipeDB(RecipeBase):
    id: int

    class Config:
        orm_mode = True
