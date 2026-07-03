from dataclasses import dataclass

from modules.notifications.application.ports.notification_delivery_repository import NotificationReadRepository
from src.modules.notifications.application.queries.list_my_notifications import ListMyNotificationsQuery
from src.modules.notifications.application.read_models import NotificationReadModel

@dataclass
class ListMyNotificationsQueryHandler:
    repo: NotificationReadRepository
    
    async def handle(self, query: ListMyNotificationsQuery) -> list[NotificationReadModel]:
        return await self.repo.get_by_user_id(query.user_id, limit=query.limit, offset=query.offset, is_read=query.is_read)