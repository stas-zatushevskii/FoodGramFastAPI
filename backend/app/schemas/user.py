from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.recipe import RecipeGet


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    username: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserRecipes(BaseModel):
    first_name: str
    last_name: str
    username: str
    id: int
    email: EmailStr
    is_subscribed: Optional[bool]
    recipes: Optional[list[RecipeGet]]
    recipes_count: Optional[int]

    class Config:
        orm_mode = True


class AuthTokenResponse(BaseModel):
    auth_token: str
