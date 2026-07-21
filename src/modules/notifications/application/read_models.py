from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class NotificationReadModel:
    id: UUID
    recipient_id: UUID
    notification_type: str
    title: str
    message: str
    source_event_id: UUID
    is_read: bool
    created_at: datetime
    read_at: datetime | None