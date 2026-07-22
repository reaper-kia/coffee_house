from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from uuid import UUID

import pytest

from src.modules.customer_requests.domain.entities import (
    CustomerRequest,
    CustomerRequestItem,
)
from src.modules.customer_requests.domain.enums import (
    CustomerRequestStatus,
    CustomerRequestType,
)
from src.modules.customer_requests.infra.repositories import (
    SQLAlchemyCustomerRequestRepository,
)
from src.modules.users.infra.repositories import SQLAlchemyUserRepository


USER_ID = UUID("82000000-0000-0000-0000-000000000001")
REQUEST_ID = UUID("82000000-0000-0000-0000-000000000002")
ITEM_ID = UUID("82000000-0000-0000-0000-000000000003")


@pytest.mark.unit
def test_user_repository_mapper_preserves_admin_flag() -> None:
    model = SimpleNamespace(
        id=USER_ID,
        name="Admin",
        email="admin@example.com",
        password_hash="hash",
        is_admin=True,
    )

    user = SQLAlchemyUserRepository._to_domain(model)

    assert user.is_admin is True


@pytest.mark.unit
def test_customer_request_repository_roundtrip() -> None:
    request = CustomerRequest(
        id=REQUEST_ID,
        request_type=CustomerRequestType.PREORDER,
        customer_name="Alice",
        contact="+49123",
        desired_datetime=datetime(2026, 8, 1, 18, tzinfo=UTC),
        person_count=2,
        comment=None,
        telegram_chat_id="12345",
        status=CustomerRequestStatus.CONFIRMED,
        _items=[
            CustomerRequestItem(
                menu_item_id=ITEM_ID,
                title_snapshot="Latte",
                price_amount_snapshot=Decimal("4.50"),
                price_currency_snapshot="EUR",
                quantity=2,
            )
        ],
    )

    model = SQLAlchemyCustomerRequestRepository._to_model(request)
    restored = SQLAlchemyCustomerRequestRepository._to_domain(model)

    assert restored.id == request.id
    assert restored.status is CustomerRequestStatus.CONFIRMED
    assert restored.items[0].title_snapshot == "Latte"
    assert restored.items[0].price_amount_snapshot == Decimal("4.50")
