from typing import Optional

from pydantic import BaseModel, Field, FilePath
from datetime import datetime
from .ingredient import Ingredient, IngredientInRecipe
from .user import UserGet
from fastapi import UploadFile


class RecipeBase(BaseModel):
    image: Optional[str]
    name: str
    description: str
    cooking_time: datetime


class RecipeCreate(RecipeBase):
    ingredients: Optional[list[IngredientInRecipe]]
    tags: Optional[list[int]]
    author: int


class RecipeUpdate(RecipeBase):
    ingredients: list[Ingredient]
    tags: list[int]


class RecipeGet(RecipeBase):
    id: int
    is_favorite: bool
    is_in_shopping_cart: bool
    author: UserGet

    class Config:
        orm_mode = True


class RecipeDB(RecipeBase):
    id: int
    author: int
    is_favorite: Optional[bool] = False
    is_in_shopping_cart: Optional[bool] = False
    tags: Optional[list[int]]

    class Config:
        orm_mode = True


class RecipeList(BaseModel):
    count: Optional[int] = 0
    next: str
    pervious: str
    results: list[RecipeDB]
    author: Optional[int]

    class Config:
        orm_mode = True