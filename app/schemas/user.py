from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    username: str
    full_name: str


class UserUpdate(BaseUser):
    username: Optional[str]
    password: Optional[str]
    full_name: Optional[str]


class UserCreate(BaseUser):
    username: str
    password: str
