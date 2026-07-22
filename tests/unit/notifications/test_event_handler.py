from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.modules.notifications.application.exceptions import (
    InvalidIntegrationEvent,
    UnsupportedIntegrationEvent,
)
from src.modules.notifications.application.handlers.handle_customer_request_event import (
    HandleCustomerRequestEventHandler,
)
from src.modules.notifications.application.services.customer_request_message_builder import (
    CustomerRequestMessageBuilder,
)
from src.modules.notifications.domain.enums import NotificationDeliveryStatus
from src.shared.events.customer_request_event import (
    CUSTOMER_REQUEST_AGGREGATE,
    CUSTOMER_REQUEST_STATUS_CHANGED,
)
from src.shared.infra.kafka.consumer import KafkaConsumedMessage
from tests.fakes import FakeUoW, FakeUoWFactory


EVENT_ID = UUID("61000000-0000-0000-0000-000000000001")
REQUEST_ID = UUID("61000000-0000-0000-0000-000000000002")


def event_payload(*, status: str = "CONFIRMED") -> dict:
    return {
        "event_id": str(EVENT_ID),
        "event_type": CUSTOMER_REQUEST_STATUS_CHANGED,
        "event_version": 1,
        "aggregate_type": CUSTOMER_REQUEST_AGGREGATE,
        "aggregate_id": str(REQUEST_ID),
        "payload": {
            "customer_request_id": str(REQUEST_ID),
            "customer_telegram_chat_id": "12345",
            "new_status": status,
            "request_type": "TABLE_BOOKING",
            "desired_datetime": None,
            "persons_count": 2,
            "comment": None,
        },
    }


def consumed(value: dict) -> KafkaConsumedMessage:
    return KafkaConsumedMessage(
        topic="events",
        partition=0,
        offset=10,
        key=str(REQUEST_ID),
        value=value,
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_handler_skips_already_processed_event() -> None:
    processed = SimpleNamespace(exists=AsyncMock(return_value=True), add=AsyncMock())
    uow = FakeUoW(processed_kafka_messages=processed)
    sender = SimpleNamespace(send=AsyncMock())
    handler = HandleCustomerRequestEventHandler(
        FakeUoWFactory(uow),
        sender,
        CustomerRequestMessageBuilder(),
        "group",
    )

    await handler.handle(consumed(event_payload()))

    sender.send.assert_not_awaited()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_handler_sends_and_marks_delivery() -> None:
    delivery_store = {}

    async def get_delivery(**kwargs):
        return delivery_store.get("delivery")

    async def add_delivery(delivery):
        delivery_store["delivery"] = delivery

    processed_repo = SimpleNamespace(
        exists=AsyncMock(return_value=False),
        add=AsyncMock(),
    )
    deliveries = SimpleNamespace(
        get_by_event_channel_recipient=AsyncMock(side_effect=get_delivery),
        add=AsyncMock(side_effect=add_delivery),
        save=AsyncMock(),
    )
    uow = FakeUoW(
        processed_kafka_messages=processed_repo,
        notification_deliveries=deliveries,
    )
    sender = SimpleNamespace(send=AsyncMock())
    handler = HandleCustomerRequestEventHandler(
        FakeUoWFactory(uow),
        sender,
        CustomerRequestMessageBuilder(),
        "group",
    )

    await handler.handle(consumed(event_payload()))

    sender.send.assert_awaited_once()
    assert delivery_store["delivery"].status is NotificationDeliveryStatus.SENT
    deliveries.save.assert_awaited_once_with(delivery_store["delivery"])
    processed_repo.add.assert_awaited_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_handler_marks_failed_delivery_and_reraises() -> None:
    delivery_store = {}

    async def get_delivery(**kwargs):
        return delivery_store.get("delivery")

    async def add_delivery(delivery):
        delivery_store["delivery"] = delivery

    deliveries = SimpleNamespace(
        get_by_event_channel_recipient=AsyncMock(side_effect=get_delivery),
        add=AsyncMock(side_effect=add_delivery),
        save=AsyncMock(),
    )
    uow = FakeUoW(
        processed_kafka_messages=SimpleNamespace(
            exists=AsyncMock(return_value=False),
            add=AsyncMock(),
        ),
        notification_deliveries=deliveries,
    )
    sender = SimpleNamespace(send=AsyncMock(side_effect=RuntimeError("down")))
    handler = HandleCustomerRequestEventHandler(
        FakeUoWFactory(uow),
        sender,
        CustomerRequestMessageBuilder(),
        "group",
    )

    with pytest.raises(RuntimeError, match="down"):
        await handler.handle(consumed(event_payload()))

    assert delivery_store["delivery"].status is NotificationDeliveryStatus.FAILED
    assert delivery_store["delivery"].last_error == "down"


@pytest.mark.unit
def test_handler_rejects_invalid_event() -> None:
    handler = HandleCustomerRequestEventHandler(
        FakeUoWFactory(FakeUoW()),
        SimpleNamespace(send=AsyncMock()),
        CustomerRequestMessageBuilder(),
        "group",
    )

    with pytest.raises(InvalidIntegrationEvent):
        handler._validate_event({"event_id": str(EVENT_ID)})


@pytest.mark.unit
def test_handler_rejects_unsupported_event_version() -> None:
    payload = event_payload()
    payload["event_version"] = 2
    handler = HandleCustomerRequestEventHandler(
        FakeUoWFactory(FakeUoW()),
        SimpleNamespace(send=AsyncMock()),
        CustomerRequestMessageBuilder(),
        "group",
    )

    with pytest.raises(UnsupportedIntegrationEvent):
        handler._validate_event(payload)
