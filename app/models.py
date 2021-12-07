"""
SQL Alchemy models declaration.

Note, imported by alembic migrations logic, see `alembic/env.py`
"""

from typing import Any

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql import false
from sqlalchemy.orm.decl_api import declarative_base


Base: Any = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(254), unique=True, index=True, nullable=False)
    full_name = Column(String(254), nullable=True)
    hashed_password = Column(String(128), nullable=False)
    is_maintainer = Column(
        Boolean, default=False, nullable=False, server_default=false()
    )
    is_root = Column(Boolean, default=False, nullable=False, server_default=false())
