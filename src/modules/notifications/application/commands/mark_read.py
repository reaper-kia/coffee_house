from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class MarkReadNotificationCommand:
    notification_id: UUID
    user_id: UUID