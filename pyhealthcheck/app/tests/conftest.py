import asyncio
from typing import Any, AsyncGenerator, Optional

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_password_hash
from app.main import app
from app.models import Base, User
from app.session import async_engine, async_session
from app.tests import utils


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine.url) == settings.TEST_SQLALCHEMY_DATABASE_URI

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest.fixture
async def session(
    test_db_setup_sessionmaker: Any,
) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_setup_sessionmaker() as session:
        yield session


@pytest.fixture
async def default_user(session: AsyncSession):
    return await utils.create_user(session)


@pytest.fixture
async def root_user(session: AsyncSession):
    return await utils.create_user(session, "root")


@pytest.fixture
async def maintainer_user(session: AsyncSession):
    return await utils.create_user(session, "maintainer")


@pytest.fixture
async def worker_user(session: AsyncSession):
    return await utils.create_user(session, "worker")


@pytest.fixture
async def get_headers(client: AsyncClient):
    async def _get_headers(user: User):
        return await utils.get_header_for_user(user, client)

    return _get_headers
