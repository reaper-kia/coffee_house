from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from src.shared.domain.exceptions import InvalidCurrencyError, NegativeAmountError
from src.shared.domain.value_objects import Money
from src.shared.events.customer_request_event import (
    CUSTOMER_REQUEST_CREATED,
    CUSTOMER_REQUEST_STATUS_CHANGED,
    create_customer_request_created_event,
    create_customer_request_status_changed_event,
)


REQUEST_ID = UUID("10000000-0000-0000-0000-000000000001")
ADMIN_ID = UUID("10000000-0000-0000-0000-000000000002")
ITEM_ID = UUID("10000000-0000-0000-0000-000000000003")


@pytest.mark.unit
def test_money_normalizes_currency() -> None:
    money = Money(Decimal("10.50"), " eur ")

    assert money.amount == Decimal("10.50")
    assert money.currency == "EUR"


@pytest.mark.unit
@pytest.mark.parametrize("currency", ["RUB", "GBP", ""])
def test_money_rejects_unsupported_currency(currency: str) -> None:
    with pytest.raises(InvalidCurrencyError):
        Money(Decimal("1"), currency)


@pytest.mark.unit
def test_money_rejects_negative_amount() -> None:
    with pytest.raises(NegativeAmountError):
        Money(Decimal("-0.01"), "EUR")


@pytest.mark.unit
def test_created_event_serializes_snapshot_items() -> None:
    event = create_customer_request_created_event(
        request_id=REQUEST_ID,
        request_type="PREORDER",
        customer_name="Alex",
        contact="+49123",
        desired_datetime=datetime(2026, 8, 1, 12, tzinfo=UTC),
        persons_count=2,
        comment="Window table",
        status="NEW",
        items=[
            {
                "menu_item_id": ITEM_ID,
                "title": "Latte",
                "quantity": 2,
                "price_amount": Decimal("4.50"),
                "price_currency": "EUR",
                "comment": None,
            }
        ],
    )

    payload = event.to_payload()

    assert payload["event_type"] == CUSTOMER_REQUEST_CREATED
    assert payload["aggregate_id"] == str(REQUEST_ID)
    assert payload["payload"]["items"] == [
        {
            "menu_item_id": str(ITEM_ID),
            "title": "Latte",
            "quantity": 2,
            "price_amount": "4.50",
            "price_currency": "EUR",
            "comment": None,
        }
    ]


@pytest.mark.unit
def test_status_event_contains_admin_and_recipient() -> None:
    event = create_customer_request_status_changed_event(
        request_id=REQUEST_ID,
        request_type="TABLE_BOOKING",
        old_status="NEW",
        new_status="CONFIRMED",
        customer_telegram_chat_id="12345",
        changed_by_admin_id=ADMIN_ID,
        changed_at=datetime(2026, 8, 1, 10, tzinfo=UTC),
        customer_name="Alex",
        desired_datetime=datetime(2026, 8, 2, 18, tzinfo=UTC),
        persons_count=4,
        comment=None,
    )

    payload = event.to_payload()

    assert payload["event_type"] == CUSTOMER_REQUEST_STATUS_CHANGED
    assert payload["payload"]["customer_telegram_chat_id"] == "12345"
    assert payload["payload"]["changed_by_admin_id"] == str(ADMIN_ID)
