from datetime import UTC, datetime

import pytest

from src.modules.customer_requests.api.dependencies import (
    get_customer_requests_mediator,
)
from src.modules.customer_requests.domain.exceptions import MenuItemUnavailable
from tests.factories import ITEM_ID, customer_request_entity
from tests.fakes import StubMediator


DESIRED_AT = datetime(2026, 8, 1, 18, tzinfo=UTC).isoformat()


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_table_booking_without_authentication(app, client) -> None:
    mediator = StubMediator(result=customer_request_entity())
    app.dependency_overrides[get_customer_requests_mediator] = lambda: mediator

    response = await client.post(
        "/api/v1/customer-requests",
        json={
            "request_type": "TABLE_BOOKING",
            "customer_name": "Alice",
            "contact": "+49123",
            "desired_datetime": DESIRED_AT,
            "person_count": 2,
            "items": [],
        },
    )

    assert response.status_code == 201
    assert response.json()["request_type"] == "TABLE_BOOKING"
    assert response.json()["status"] == "NEW"
    assert mediator.messages[0].customer_name == "Alice"


@pytest.mark.api
@pytest.mark.asyncio
async def test_preorder_requires_item(app, client) -> None:
    app.dependency_overrides[get_customer_requests_mediator] = lambda: StubMediator()

    response = await client.post(
        "/api/v1/customer-requests",
        json={
            "request_type": "PREORDER",
            "customer_name": "Alice",
            "contact": "+49123",
            "desired_datetime": DESIRED_AT,
            "items": [],
        },
    )

    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.asyncio
async def test_unavailable_preorder_item_returns_422(app, client) -> None:
    app.dependency_overrides[get_customer_requests_mediator] = lambda: StubMediator(
        error=MenuItemUnavailable("Menu item unavailable")
    )

    response = await client.post(
        "/api/v1/customer-requests",
        json={
            "request_type": "PREORDER",
            "customer_name": "Alice",
            "contact": "+49123",
            "desired_datetime": DESIRED_AT,
            "items": [{"menu_item_id": str(ITEM_ID), "quantity": 1}],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Menu item unavailable"
