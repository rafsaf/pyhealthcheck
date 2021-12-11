from typing import Optional

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean


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
    username: Optional[str]
    password: Optional[str]
    full_name: Optional[str]


class UserCreate(BaseUser):
    username: str
    password: str


class WorkerUserCreate(BaseUser):
    register_key: str


class UserGet(BaseUser):
    username: str
