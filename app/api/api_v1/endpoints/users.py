from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session
from sqlalchemy import select
from app import models, schemas
from .. import deps
from app.core.security import get_password_hash
from app.models import User

router = APIRouter(prefix="/users")


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    user_update: schemas.UserUpdate,
    session: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_normal_user),
):
    """
    Update current user.
    """

    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)  # type: ignore
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name  # type: ignore
    if user_update.username is not None:
        current_user.username = user_update.username  # type: ignore

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return current_user


@router.get("/me", response_model=schemas.User)
async def read_user_me(current_user: models.User = Depends(deps.get_normal_user)):
    """
    Get current user.
    """
    return current_user


@router.get("/{username}", response_model=schemas.User)
async def read_user(
    username: str,
    current_user: models.User = Depends(deps.get_maintainer_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Get user by username. Maintainer permission is required.
    """
    user_result = await session.execute(select(User).where(User.username == username))
    user = user_result.scalars().first()
    if user is None:
        return JSONResponse(
            status_code=404,
            content={"message": "User not found"},
        )
    return user


@router.get("", response_model=list[schemas.User])
async def read_all_users(
    offset: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_maintainer_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Get all users. Maintainer permission is required.
    """
    users_result = await session.execute(select(User).offset(offset).limit(limit))
    return users_result.scalars().all()


@router.delete("/me", response_model=None, status_code=204)
async def read_delete_me(
    current_user: models.User = Depends(deps.get_normal_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Delete current user.
    """
    await session.delete(current_user)
    await session.commit()
    return None
