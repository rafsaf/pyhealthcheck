from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core import security
from app.core.config import settings
from app.models import User
from app.session import async_session

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"v1/auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> User:

    try:
        payload = jwt.decode(  # type: ignore
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user: Optional[User] = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_normal_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


async def get_maintainer_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_maintainer and not current_user.is_root:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return current_user


async def get_root_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_root:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return current_user
