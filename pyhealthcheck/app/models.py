"""
SQL Alchemy models declaration.

Note, imported by alembic migrations logic, see `alembic/env.py`
"""

from typing import Any

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.sql import false, null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY

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
    is_worker = Column(Boolean, default=False, nullable=False, server_default=false())
    healthstacks = relationship(
        "HealthStack", back_populates="user", foreign_keys="HealthStack.user_id"
    )
    healthstack_job = relationship(
        "HealthStack",
        back_populates="worker",
        uselist=False,
        foreign_keys="HealthStack.worker_id",
    )


class HealthStack(Base):
    __tablename__ = "healthstack"
    id = Column(Integer, primary_key=True, index=True)
    custom_name = Column(
        String(254), nullable=True, default=None, server_default=null()
    )
    domains = Column(ARRAY(String(100)), nullable=False)
    delay_between_checks = Column(Integer, nullable=False)
    emails_to_alert = Column(ARRAY(String(128)), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE", name="user_id_fk"),
        nullable=False,
    )
    worker_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="SET NULL", name="worker_id_fk"),
        nullable=True,
        default=None,
        server_default=null(),
    )
    user = relationship(
        "User", back_populates="healthstacks", foreign_keys="HealthStack.user_id"
    )
    worker = relationship(
        "User", back_populates="healthstack_job", foreign_keys="HealthStack.worker_id"
    )
