import random
import string
from typing import Literal

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models import User
from app.main import app


def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email(length: int = 10) -> str:
    return f"{random_lower_string(length)}@{random_lower_string(length)}.com"


def reverse(view_function_name: str) -> str:
    # for route in app.routes:
    #    print(route.__dict__["path"])
    return app.url_path_for(view_function_name)


async def create_user(
    session: AsyncSession,
    additional_permission: Literal["root", "maintainer", "worker", "normal"] = "normal",
) -> User:
    new_user = User(
        username=random_lower_string(),
        hashed_password=get_password_hash("password"),
        full_name=random_lower_string(),
    )
    if additional_permission == "root":
        new_user.is_root = True  # type: ignore
    elif additional_permission == "worker":
        new_user.is_worker = True  # type: ignore
    elif additional_permission == "maintainer":
        new_user.is_maintainer = True  # type: ignore

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_header_for_user(user: User, client: AsyncClient):
    access_token = await client.post(
        reverse("login_access_token"),
        data={
            "username": user.username,
            "password": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return {"Authorization": f"Bearer {access_token.json()['access_token']}"}
