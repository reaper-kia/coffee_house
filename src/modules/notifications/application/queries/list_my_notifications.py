from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ListMyNotificationsQuery:
    user_id: UUID
    offset: int = 0
    limit: int = 20 
    is_read: bool | None = None