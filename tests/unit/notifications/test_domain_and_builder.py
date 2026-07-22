from uuid import UUID

import pytest

from src.modules.notifications.application.services.customer_request_message_builder import (
    CustomerRequestMessageBuilder,
)
from src.modules.notifications.domain.delivery import NotificationDelivery
from src.modules.notifications.domain.enums import (
    NotificationChannel,
    NotificationDeliveryStatus,
)
from src.shared.events.customer_request_event import (
    CUSTOMER_REQUEST_CREATED,
    CUSTOMER_REQUEST_STATUS_CHANGED,
)


EVENT_ID = UUID("60000000-0000-0000-0000-000000000001")
REQUEST_ID = UUID("60000000-0000-0000-0000-000000000002")


@pytest.mark.unit
def test_notification_delivery_lifecycle() -> None:
    delivery = NotificationDelivery(
        event_id=EVENT_ID,
        channel=NotificationChannel.TELEGRAM,
        recipient="12345",
        message="hello",
        customer_request_id=REQUEST_ID,
    )

    delivery.mark_failed(error="network")
    assert delivery.status is NotificationDeliveryStatus.FAILED
    assert delivery.attempts == 1
    assert delivery.last_error == "network"

    delivery.mark_sent()
    assert delivery.status is NotificationDeliveryStatus.SENT
    assert delivery.sent_at is not None
    assert delivery.last_error is None


@pytest.mark.unit
def test_message_builder_builds_confirmed_message() -> None:
    message = CustomerRequestMessageBuilder().build(
        event={
            "event_type": CUSTOMER_REQUEST_STATUS_CHANGED,
            "payload": {
                "new_status": "CONFIRMED",
                "request_type": "TABLE_BOOKING",
                "desired_datetime": "2026-08-01T18:00:00+00:00",
                "persons_count": 4,
                "comment": "Window",
            },
        }
    )

    assert "подтверждена" in message
    assert "бронь столика" in message
    assert "Гостей: 4" in message


@pytest.mark.unit
def test_message_builder_builds_cancelled_message() -> None:
    message = CustomerRequestMessageBuilder().build(
        event={
            "event_type": CUSTOMER_REQUEST_STATUS_CHANGED,
            "payload": {
                "new_status": "CANCELLED",
                "request_type": "PREORDER",
                "desired_datetime": None,
                "comment": None,
            },
        }
    )

    assert "отменена" in message
    assert "предзаказ" in message


@pytest.mark.unit
def test_message_builder_ignores_created_event() -> None:
    assert (
        CustomerRequestMessageBuilder().build(
            event={"event_type": CUSTOMER_REQUEST_CREATED, "payload": {}}
        )
        is None
    )
