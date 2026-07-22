
import pytest

from src.modules.auth.api.dependencies import get_current_user_id
from src.modules.users.api.dependencies import get_mediator
from src.modules.auth.api.rate_limit import limit_register_request
from src.modules.users.domain.entities import User
from src.modules.users.domain.exceptions import EmailAlreadyExistError, UserNotFoundError
from src.modules.users.domain.value_objects import Email, UserName
from tests.factories import USER_ID, user_read_model
from tests.fakes import StubMediator


async def allow_request() -> None:
    return None


@pytest.mark.api
@pytest.mark.asyncio
async def test_register_user(app, client) -> None:
    user = User.register(
        UserName("Alice"),
        Email("alice@example.com"),
        "hash",
    )
    user.id = USER_ID
    mediator = StubMediator(result=user)
    app.dependency_overrides[get_mediator] = lambda: mediator
    app.dependency_overrides[limit_register_request] = allow_request

    response = await client.post(
        "/users/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": str(USER_ID),
        "name": "Alice",
        "email": "alice@example.com",
        "is_admin": False,
    }
    assert mediator.messages[0].email == "alice@example.com"


@pytest.mark.api
@pytest.mark.asyncio
async def test_register_duplicate_email_returns_conflict(app, client) -> None:
    app.dependency_overrides[get_mediator] = lambda: StubMediator(
        error=EmailAlreadyExistError("Email already registered")
    )
    app.dependency_overrides[limit_register_request] = allow_request

    response = await client.post(
        "/users/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_me_returns_user_read_model(app, client) -> None:
    app.dependency_overrides[get_current_user_id] = lambda: USER_ID
    app.dependency_overrides[get_mediator] = lambda: StubMediator(
        result=user_read_model()
    )

    response = await client.get("/users/me")

    assert response.status_code == 200
    assert response.json()["id"] == str(USER_ID)
    assert response.json()["name"] == "Alice"


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_user_not_found(app, client) -> None:
    app.dependency_overrides[get_mediator] = lambda: StubMediator(
        error=UserNotFoundError("User not found")
    )

    response = await client.get(f"/users/{USER_ID}")

    assert response.status_code == 404
