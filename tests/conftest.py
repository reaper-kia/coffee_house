from __future__ import annotations

import os
from collections.abc import AsyncIterator
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

# Settings are instantiated during module import, so test defaults must exist first.
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("ADMIN_REGISTRATION_CODE", "test-admin-code")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "coffee_house_test")
os.environ.setdefault("POSTGRES_USER", "coffee_house")
os.environ.setdefault("POSTGRES_PASSWORD", "coffee_house")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://coffee_house:coffee_house@localhost:5432/coffee_house_test",
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/15")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token")

from src.main import create_app  # noqa: E402
from src.modules.auth.api.dependencies import CurrentUser  # noqa: E402


ADMIN_ID = UUID("00000000-0000-0000-0000-000000000001")
USER_ID = UUID("00000000-0000-0000-0000-000000000002")


@pytest.fixture
def app():
    application = create_app()
    yield application
    application.dependency_overrides.clear()


@pytest.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as test_client:
        yield test_client


@pytest.fixture
def admin_user() -> CurrentUser:
    return CurrentUser(id=ADMIN_ID, is_admin=True)


@pytest.fixture
def regular_user() -> CurrentUser:
    return CurrentUser(id=USER_ID, is_admin=False)
