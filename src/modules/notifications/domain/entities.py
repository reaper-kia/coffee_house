from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.modules.customer_requests.domain.enums import CustomerRequestType
from src.modules.notifications.domain.enums import NotificationType


@dataclass 
class Notification:
    recipient_id: UUID
    notification_type: NotificationType 
    title: str
    message: str
    source_event_id: UUID
    id: UUID = field(default_factory=uuid4)
    is_read: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    read_at: datetime | None = None
    
    @classmethod
    def create(
        cls, *, recipient_id: UUID, notification_type: NotificationType, title: str, source_event_id: UUID, message: str,
    ) -> "Notification":
        return cls(
            recipient_id=recipient_id,
            notification_type=notification_type,
            title=title,
            message=message,
            source_event_id=source_event_id,
        )
    
    @classmethod
    def create_cutomer_request(
        cls, *, recipient_id: UUID, request_id: UUID, request_type: CustomerRequestType, customer_name: str, source_event_id: UUID,
    ) -> "Notification":
        return cls.create(
            recipient_id=recipient_id,
            notification_type=NotificationType.CUSTOMER_REQUEST,
            title=f"Customer request {request_type.value}",
            message=f"Customer {customer_name} make request {request_type.value} with id: {request_id}",
            source_event_id=source_event_id,
        )
    
    def mark_read(self) -> None:
        if self.is_read:
            return
        
        self.is_read = True
        self.read_at = datetime.now(UTC)