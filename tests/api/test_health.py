from unittest.mock import AsyncMock

import pytest

from src.shared.infra.database.session import get_async_session
from src.shared.infra.redis.dependencies import get_redis_client


@pytest.mark.api
@pytest.mark.asyncio
async def test_basic_health(client) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "success"}


@pytest.mark.api
@pytest.mark.asyncio
async def test_database_health(app, client, monkeypatch) -> None:
    app.dependency_overrides[get_async_session] = lambda: object()
    check = AsyncMock(return_value=True)
    monkeypatch.setattr("src.main.check_database_connection", check)

    response = await client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"database": "ok"}
    check.assert_awaited_once()


@pytest.mark.api
@pytest.mark.asyncio
async def test_redis_health_reports_error(app, client, monkeypatch) -> None:
    app.dependency_overrides[get_redis_client] = lambda: object()
    check = AsyncMock(return_value=False)
    monkeypatch.setattr("src.main.check_redis_connection", check)

    response = await client.get("/health/redis")

    assert response.status_code == 200
    assert response.json() == {"redis": "error"}
