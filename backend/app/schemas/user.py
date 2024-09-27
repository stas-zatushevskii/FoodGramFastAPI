from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


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


class UserGet(BaseModel):
    first_name: str
    last_name: str
    username: str
    id: int
    email: EmailStr
    is_subscribed: bool