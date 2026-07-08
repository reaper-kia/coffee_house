from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.modules.notifications.domain.enums import (
    NotificationChannel,
    NotificationDeliveryStatus,
)


@dataclass
class NotificationDelivery:
    event_id: UUID
    channel: NotificationChannel
    recipient: str
    message: str
    customer_request_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    status: NotificationDeliveryStatus = NotificationDeliveryStatus.PENDING
    attempts: int = 0
    last_error: str | None = None
    sent_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mark_sent(self) -> None:
        now = datetime.now(UTC)

        self.status = NotificationDeliveryStatus.SENT
        self.sent_at = now
        self.last_error = None
        self.updated_at = now

    def mark_failed(self, *, error: str) -> None:
        now = datetime.now(UTC)

        self.status = NotificationDeliveryStatus.FAILED
        self.attempts += 1
        self.last_error = error
        self.updated_at = now