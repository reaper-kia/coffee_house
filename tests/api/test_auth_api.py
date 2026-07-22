import pytest

from src.modules.auth.api.dependencies import get_auth_mediator
from src.modules.auth.api.rate_limit import limit_login_request
from src.modules.auth.application.exceptions import InvalidCredentialError
from tests.fakes import StubMediator


async def allow_request() -> None:
    return None


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_sets_access_cookie(app, client) -> None:
    mediator = StubMediator(result="signed-token")
    app.dependency_overrides[get_auth_mediator] = lambda: mediator
    app.dependency_overrides[limit_login_request] = allow_request

    response = await client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Logged in"}
    assert "access_token=signed-token" in response.headers["set-cookie"]
    assert "HttpOnly" in response.headers["set-cookie"]
    assert mediator.messages[0].email == "user@example.com"


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_rejects_invalid_credentials(app, client) -> None:
    app.dependency_overrides[get_auth_mediator] = lambda: StubMediator(
        error=InvalidCredentialError("Invalid email or password")
    )
    app.dependency_overrides[limit_login_request] = allow_request

    response = await client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.api
@pytest.mark.asyncio
async def test_logout_deletes_cookie(client) -> None:
    response = await client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json() == {"message": "Logged out"}
    assert "Max-Age=0" in response.headers["set-cookie"]
