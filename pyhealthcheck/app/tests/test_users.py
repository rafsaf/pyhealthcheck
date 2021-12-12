import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.tests.utils import random_lower_string, reverse
from app.models import User

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.asyncio


async def test_read_user_me(client: AsyncClient, default_user: User, get_headers):
    headers = await get_headers(default_user)
    result = await client.get(reverse("read_user_me"))

    assert result.status_code == 401

    result2 = await client.get(reverse("read_user_me"), headers=headers)
    assert result2.status_code == 200
    assert result2.json()["username"] == default_user.username


async def test_update_user_me(
    client: AsyncClient, default_user: User, get_headers, session: AsyncSession
):
    headers = await get_headers(default_user)
    to_update = {"password": "too_easy_password", "full_name": random_lower_string()}
    result = await client.put(reverse("update_user_me"), json=to_update)

    assert result.status_code == 401

    result = await client.put(
        reverse("update_user_me"), headers=headers, json=to_update
    )
    assert result.status_code == 404

    to_update["password"] = "zaq1@WSX!23$."
    result = await client.put(
        reverse("update_user_me"), headers=headers, json=to_update
    )
    assert result.status_code == 200
    await session.refresh(default_user)
    assert result.json()["full_name"] == default_user.full_name
    assert result.json()["full_name"] == to_update["full_name"]
