from datetime import UTC, datetime
from decimal import Decimal
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
from src.modules.customer_requests.domain.exceptions import (
    CustomerRequestEmptyError,
    CustomerRequestInvalidPersonCountError,
    CustomerRequestInvalidTypeError,
    CustomerRequestItemInvalidCommentError,
    CustomerRequestItemInvalidPriceError,
    CustomerRequestItemInvalidQuantityError,
    CustomerRequestStatusInvalidTransition,
)


ITEM_ID = UUID("50000000-0000-0000-0000-000000000001")
DESIRED_AT = datetime(2026, 8, 1, 18, tzinfo=UTC)


def make_item(**overrides) -> CustomerRequestItem:
    values = {
        "menu_item_id": ITEM_ID,
        "title_snapshot": "Latte",
        "price_amount_snapshot": Decimal("4.50"),
        "price_currency_snapshot": "eur",
        "quantity": 2,
        "comment": " No sugar ",
    }
    values.update(overrides)
    return CustomerRequestItem(**values)


@pytest.mark.unit
def test_request_item_normalizes_snapshot() -> None:
    item = make_item()

    assert item.title_snapshot == "Latte"
    assert item.price_currency_snapshot == "EUR"
    assert item.comment == "No sugar"


@pytest.mark.unit
@pytest.mark.parametrize("quantity", [0, -1, 101])
def test_request_item_rejects_invalid_quantity(quantity: int) -> None:
    with pytest.raises(CustomerRequestItemInvalidQuantityError):
        make_item(quantity=quantity)


@pytest.mark.unit
def test_request_item_rejects_non_positive_price() -> None:
    with pytest.raises(CustomerRequestItemInvalidPriceError):
        make_item(price_amount_snapshot=Decimal("0"))


@pytest.mark.unit
def test_request_item_rejects_long_comment() -> None:
    with pytest.raises(CustomerRequestItemInvalidCommentError):
        make_item(comment="x" * 501)


@pytest.mark.unit
def test_preorder_requires_items() -> None:
    with pytest.raises(CustomerRequestInvalidTypeError):
        CustomerRequest.create(
            request_type=CustomerRequestType.PREORDER,
            customer_name="Alice",
            contact="+49123",
            desired_datetime=DESIRED_AT,
            items=[],
        )


@pytest.mark.unit
def test_non_preorder_rejects_items() -> None:
    with pytest.raises(CustomerRequestInvalidTypeError):
        CustomerRequest.create(
            request_type=CustomerRequestType.TABLE_BOOKING,
            customer_name="Alice",
            contact="+49123",
            desired_datetime=DESIRED_AT,
            items=[make_item()],
        )


@pytest.mark.unit
@pytest.mark.parametrize("name,contact", [(" ", "+49123"), ("Alice", " ")])
def test_request_requires_customer_identity(name: str, contact: str) -> None:
    with pytest.raises(CustomerRequestEmptyError):
        CustomerRequest.create(
            request_type=CustomerRequestType.TABLE_BOOKING,
            customer_name=name,
            contact=contact,
            desired_datetime=DESIRED_AT,
            items=[],
        )


@pytest.mark.unit
@pytest.mark.parametrize("person_count", [0, 501])
def test_request_validates_person_count(person_count: int) -> None:
    with pytest.raises(CustomerRequestInvalidPersonCountError):
        CustomerRequest.create(
            request_type=CustomerRequestType.TABLE_BOOKING,
            customer_name="Alice",
            contact="+49123",
            desired_datetime=DESIRED_AT,
            person_count=person_count,
            items=[],
        )


@pytest.mark.unit
def test_request_normalizes_optional_text() -> None:
    request = CustomerRequest.create(
        request_type=CustomerRequestType.TABLE_BOOKING,
        customer_name=" Alice ",
        contact=" +49123 ",
        desired_datetime=DESIRED_AT,
        person_count=2,
        comment=" Window ",
        telegram_chat_id=" 12345 ",
        items=[],
    )

    assert request.customer_name == "Alice"
    assert request.contact == "+49123"
    assert request.comment == "Window"
    assert request.telegram_chat_id == "12345"


@pytest.mark.unit
def test_request_status_transitions() -> None:
    request = CustomerRequest.create(
        request_type=CustomerRequestType.TABLE_BOOKING,
        customer_name="Alice",
        contact="+49123",
        desired_datetime=DESIRED_AT,
        items=[],
    )

    request.change_status(CustomerRequestStatus.CONFIRMED)
    request.change_status(CustomerRequestStatus.DONE)

    assert request.status is CustomerRequestStatus.DONE


@pytest.mark.unit
def test_request_rejects_invalid_status_transition() -> None:
    request = CustomerRequest.create(
        request_type=CustomerRequestType.TABLE_BOOKING,
        customer_name="Alice",
        contact="+49123",
        desired_datetime=DESIRED_AT,
        items=[],
    )

    with pytest.raises(CustomerRequestStatusInvalidTransition):
        request.change_status(CustomerRequestStatus.DONE)
