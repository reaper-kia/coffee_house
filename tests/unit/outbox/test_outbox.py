from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.shared.events.integration_event import IntegrationEvent
from src.shared.outbox.application.publisher import OutboxPublisher
from src.shared.outbox.domain.entities import OutboxMessage
from src.shared.outbox.domain.enums import OutboxMessageStatus
from tests.fakes import FakeUoW, FakeUoWFactory


AGGREGATE_ID = UUID("70000000-0000-0000-0000-000000000001")


def make_message(*, max_attempts: int = 3) -> OutboxMessage:
    event = IntegrationEvent(
        event_type="TestEvent",
        aggregate_type="Test",
        aggregate_id=AGGREGATE_ID,
        data={"value": 1},
    )
    return OutboxMessage.from_event(
        event=event,
        topic="test-events",
        key=str(AGGREGATE_ID),
        max_attempts=max_attempts,
    )


@pytest.mark.unit
def test_outbox_message_lifecycle() -> None:
    message = make_message(max_attempts=2)

    message.mark_processing(worker_id="worker")
    assert message.status is OutboxMessageStatus.PROCESSING
    assert message.locked_by == "worker"

    message.mark_failed(error="network", retry_after_seconds=5)
    assert message.status is OutboxMessageStatus.PENDING
    assert message.attempts == 1
    assert message.last_error == "network"

    message.mark_failed(error="network", retry_after_seconds=5)
    assert message.status is OutboxMessageStatus.FAILED


@pytest.mark.unit
def test_outbox_message_marks_published() -> None:
    message = make_message()
    message.mark_processing(worker_id="worker")

    message.mark_published()

    assert message.status is OutboxMessageStatus.PUBLISHED
    assert message.published_at is not None
    assert message.locked_by is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_publisher_publishes_pending_messages() -> None:
    message = make_message()
    repo = SimpleNamespace(
        get_pending_batch_for_update=AsyncMock(return_value=[message]),
        save=AsyncMock(),
    )
    uow = FakeUoW(outbox=repo)
    producer = SimpleNamespace(send_json=AsyncMock())
    publisher = OutboxPublisher(FakeUoWFactory(uow), producer, worker_id="worker")

    count = await publisher.publish_once()

    assert count == 1
    assert message.status is OutboxMessageStatus.PUBLISHED
    producer.send_json.assert_awaited_once_with(
        topic=message.topic,
        key=message.key,
        value=message.payload,
    )
    repo.save.assert_awaited_once_with(message)
    uow.commit.assert_awaited_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_publisher_keeps_failed_message_for_retry(monkeypatch) -> None:
    message = make_message()
    repo = SimpleNamespace(
        get_pending_batch_for_update=AsyncMock(return_value=[message]),
        save=AsyncMock(),
    )
    uow = FakeUoW(outbox=repo)
    producer = SimpleNamespace(send_json=AsyncMock(side_effect=RuntimeError("down")))
    monkeypatch.setattr(
        "src.shared.outbox.application.publisher.calculate_retry_delay_seconds",
        lambda attempts: 5,
    )
    publisher = OutboxPublisher(FakeUoWFactory(uow), producer, worker_id="worker")

    count = await publisher.publish_once()

    assert count == 0
    assert message.status is OutboxMessageStatus.PENDING
    assert message.attempts == 1
    assert message.last_error == "down"
    repo.save.assert_awaited_once_with(message)
