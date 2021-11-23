"""
Black-box security shortcuts to generate JWT tokens and password hash/verify

`subject` in access/refresh func may be antyhing unique to User account, `id` etc.
"""
import re
from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: Union[str, Any]) -> tuple[str, datetime]:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "refresh": False}
    encoded_jwt: str = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt, expire


def create_refresh_token(subject: Union[str, Any]) -> tuple[str, datetime]:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "refresh": True}
    encoded_jwt: str = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt, expire


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def password_strong_message(password: str) -> Optional[str]:
    """
    Verify the strength of "password"

    Returns `None` if it is strong or problem message else

    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    if len(password) < 8:
        return "Password must have 8 characters length or more"

    # searching for digits
    if re.search(r"\d", password) is None:
        return "Password must not contain digits"

    # searching for uppercase
    if re.search(r"[A-Z]", password) is None:
        return "Password must container at least one uppercase letter"

    # searching for lowercase
    if re.search(r"[a-z]", password) is None:
        return "Password must container at least one lowercase letter"

    # searching for symbols
    if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None:
        return "Password must container at least one symbol"
