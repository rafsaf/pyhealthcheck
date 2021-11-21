from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from .. import deps
from app.core import security
from app.core.config import settings
from app.models import User

router = APIRouter(prefix="/auth")


@router.post("/access-token", response_model=schemas.Token)
async def login_access_token(
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token, get an access token for future requests using username and password
    """
    result = await session.execute(
        select(User).where(User.username == form_data.username)  # type: ignore
    )
    user: Optional[User] = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not security.verify_password(form_data.password, user.hashed_password):  # type: ignore
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token, expire_at = security.create_access_token(user.id)
    refresh_token, refresh_expire_at = security.create_refresh_token(user.id)
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
        "refresh_token": refresh_token,
        "refresh_expire_at": refresh_expire_at,
    }


@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_token(
    input: schemas.TokenRefresh, session: AsyncSession = Depends(deps.get_session)
):
    """
    OAuth2 compatible token, get an access token for future requests using refresh token
    """
    try:
        payload = jwt.decode(  # type: ignore
            input.refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    result = await session.execute(select(User).where(User.id == token_data.sub))
    user: Optional[User] = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    access_token, expire_at = security.create_access_token(user.id)
    refresh_token, refresh_expire_at = security.create_refresh_token(user.id)
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
        "refresh_token": refresh_token,
        "refresh_expire_at": refresh_expire_at,
    }
