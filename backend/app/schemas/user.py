from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing import Optional


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


class UserInRecipe(BaseModel):
    first_name: str
    last_name: str
    username: str
    id: int
    email: EmailStr
    is_subscribed: Optional[bool] = False
    recipes_count: Optional[int] = 0

    class Config:
        orm_mode = True


class UserRecipes(BaseModel):
    first_name: str
    last_name: str
    username: str
    id: int
    email: EmailStr
    is_subscribed: Optional[bool] = False
    recipes_made: Optional[list] = []
    recipes_count: Optional[int] = 0

    class Config:
        orm_mode = True


class AuthTokenResponse(BaseModel):
    auth_token: str
