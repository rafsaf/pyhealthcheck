import pytest
from httpx import AsyncClient
from app.tests.utils import reverse
from app.models import User

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.asyncio


async def test_login_endpoints(client: AsyncClient, default_user: User):

    # access-token endpoint
    access_token = await client.post(
        reverse("login_access_token"),
        data={
            "username": default_user.username,
            "password": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert access_token.status_code == 200
    token = access_token.json()

    access_token = token["access_token"]
    refresh_token = token["refresh_token"]

    test_token = await client.get(
        reverse("read_user_me"), headers={"Authorization": f"Bearer {access_token}"}
    )
    assert test_token.status_code == 200
    response_user = test_token.json()
    assert response_user["username"] == default_user.username

    # refresh-token endpoint
    get_new_token = await client.post(
        reverse("refresh_token"), json={"refresh_token": refresh_token}
    )

    assert get_new_token.status_code == 200
    new_token = get_new_token.json()

    assert "access_token" in new_token
