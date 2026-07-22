import pytest

from src.modules.auth.api.dependencies import require_admin
from src.modules.customer_requests.api.dependencies import (
    get_customer_requests_mediator,
)
from src.modules.customer_requests.application.read_models import (
    CustomerRequestPageReadModel,
)
from src.modules.customer_requests.domain.enums import CustomerRequestStatus
from src.modules.customer_requests.domain.exceptions import (
    CustomerRequestNotFound,
    CustomerRequestStatusInvalidTransition,
)
from tests.factories import REQUEST_ID, customer_request_entity, customer_request_read_model
from tests.fakes import StubMediator


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_requests_require_authentication(client) -> None:
    response = await client.get("/admin/customer-requests")

    assert response.status_code == 401


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_lists_requests(app, client, admin_user) -> None:
    result = CustomerRequestPageReadModel(
        items=[customer_request_read_model()],
        total=1,
    )
    mediator = StubMediator(result=result)
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_customer_requests_mediator] = lambda: mediator

    response = await client.get(
        "/admin/customer-requests?page=1&page_size=20&status=NEW"
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["total_pages"] == 1
    assert response.json()["items"][0]["id"] == str(REQUEST_ID)
    assert mediator.messages[0].page_size == 20


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_get_request_not_found(app, client, admin_user) -> None:
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_customer_requests_mediator] = lambda: StubMediator(
        error=CustomerRequestNotFound("not found")
    )

    response = await client.get(f"/admin/customer-requests/{REQUEST_ID}")

    assert response.status_code == 404


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_changes_request_status(app, client, admin_user) -> None:
    request = customer_request_entity()
    request.change_status(CustomerRequestStatus.CONFIRMED)
    mediator = StubMediator(result=request)
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_customer_requests_mediator] = lambda: mediator

    response = await client.patch(
        f"/admin/customer-requests/{REQUEST_ID}/status?status=CONFIRMED"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMED"
    assert mediator.messages[0].changed_by_admin_id == admin_user.id


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_invalid_transition_returns_422(app, client, admin_user) -> None:
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_customer_requests_mediator] = lambda: StubMediator(
        error=CustomerRequestStatusInvalidTransition("invalid")
    )

    response = await client.patch(
        f"/admin/customer-requests/{REQUEST_ID}/status?status=DONE"
    )

    assert response.status_code == 422
