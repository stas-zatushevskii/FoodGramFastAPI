from typing import Optional

from pydantic import BaseModel, Field, FilePath
from datetime import datetime
from .ingredient import Ingredient, IngredientInRecipe
from .user import UserInRecipe
from fastapi import UploadFile
from .tag import Tag


class RecipeBase(BaseModel):
    image: Optional[str]
    name: str
    text: str
    cooking_time: int


class RecipeCreate(RecipeBase):
    ingredients: Optional[list[IngredientInRecipe]]
    tags: Optional[list[int]]


class RecipeUpdate(RecipeBase):
    ingredients: list[Ingredient]
    tags: list[int]


class RecipeGet(RecipeBase):
    id: int
    name: str
    image: str
    cooking_time: int

    class Config:
        orm_mode = True


class RecipeDB(RecipeBase):
    id: int
    tags: Optional[list[Tag]]
    author: UserInRecipe
    ingredients: Optional[list[Ingredient]]
    is_favorited: Optional[bool] = False
    is_in_shopping_cart: Optional[bool] = False
    name: Optional[str]
    text: Optional[str]
    cooking_time: Optional[str]
    image: str

    class Config:
        orm_mode = True


class RecipeList(BaseModel):
    count: Optional[int] = 0
    next: str
    pervious: str
    results: list[RecipeDB]

    class Config:
        orm_mode = True