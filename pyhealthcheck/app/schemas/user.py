from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    username: str
    full_name: Optional[str]
    is_root: bool
    is_maintainer: bool
    is_worker: bool


class UserWorkerWithPassword(User):
    password: str


class UserUpdate(BaseUser):
    password: Optional[str] = Field(max_length=32)
    full_name: Optional[str] = Field(max_length=254)


class UserUpdateAdmin(UserUpdate):
    is_root: Optional[bool]
    is_maintainer: Optional[bool]


class UserCreate(BaseUser):
    username: str = Field(max_length=254)
    password: str = Field(max_length=32)


class WorkerUserCreate(BaseUser):
    register_key: str
    healthstack_id: int


class UserGet(BaseUser):
    username: str = Field(max_length=254)
