from typing import Protocol
from uuid import UUID

from src.modules.notifications.domain.delivery import NotificationDelivery
from src.modules.notifications.domain.enums import NotificationChannel


class NotificationDeliveryRepository(Protocol):
    async def add(self, delivery: NotificationDelivery) -> NotificationDelivery:
        ...

    async def get_by_event_channel_recipient(
        self,
        *,
        event_id: UUID,
        channel: NotificationChannel,
        recipient: str,
    ) -> NotificationDelivery | None:
        ...

    async def save(self, delivery: NotificationDelivery) -> None:
        ...