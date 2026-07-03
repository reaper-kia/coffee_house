from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.notifications.application.ports.notification_delivery_repository import NotificationReadRepository, NotificationRepository
from src.modules.notifications.application.read_models import NotificationReadModel
from src.modules.notifications.domain.entities import Notification
from src.modules.notifications.domain.enums import NotificationType
from src.modules.notifications.domain.exceptions import NotificationNotFoundError
from src.modules.notifications.infra.models import NotificationModel


class SQLAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, notification: Notification) -> Notification:
        self.session.add(self._to_model(notification))
        
        return notification
        
    async def save(self, notification: Notification) -> None:
        model = await self.session.get(NotificationModel, notification.id)
        
        if model is None:
            raise NotificationNotFoundError("Notification not found.")
        
        model.recipient_id = notification.recipient_id
        model.notification_type = notification.notification_type.value
        model.title = notification.title
        model.message = notification.message
        model.source_event_id = notification.source_event_id
        model.is_read = notification.is_read
        model.created_at = notification.created_at
        model.read_at = notification.read_at
    
    async def get_by_id(self, notification_id) -> Notification | None:
        model = await self.session.get(NotificationModel, notification_id)
        
        if model is None:
            return None
        
        return self._to_entity(model)
    
    async def get_by_source_event_id(
        self,
        source_event_id: UUID,
    ) -> Notification | None:
        stmt = select(NotificationModel).where(
            NotificationModel.source_event_id == source_event_id
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)
    
    @staticmethod
    def _to_model(notification: Notification) -> NotificationModel:
        return NotificationModel(
            id=notification.id,
            recipient_id=notification.recipient_id,
            notification_type=notification.notification_type.value,
            title=notification.title,
            message=notification.message,
            source_event_id=notification.source_event_id,
            is_read=notification.is_read,
            created_at=notification.created_at,
            read_at=notification.read_at,
        )
    
    @staticmethod
    def _to_entity(model: NotificationModel) -> Notification:
        return Notification(
            id=model.id,
            recipient_id=model.recipient_id,
            notification_type=NotificationType(model.notification_type),
            title=model.title,
            message=model.message,
            source_event_id=model.source_event_id,
            is_read=model.is_read,
            created_at=model.created_at,
            read_at=model.read_at,
        )
    
class SQLAlchemyNotificationReadRepository(NotificationReadRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_user_id(self, user_id: UUID, *, limit: int = 20, offset: int = 0, is_read: bool | None = None) -> list[NotificationReadModel]:
        stmt = (
            select(
                NotificationModel.id,
                NotificationModel.recipient_id,
                NotificationModel.notification_type,
                NotificationModel.title,
                NotificationModel.message,
                NotificationModel.source_event_id,
                NotificationModel.is_read,
                NotificationModel.created_at,
                NotificationModel.read_at,
            )
            .where(NotificationModel.recipient_id == user_id)
            .order_by(NotificationModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        if is_read is not None:
            stmt = stmt.where(NotificationModel.is_read == is_read)
        
        result = await self.session.execute(stmt)
        rows = result.all()
        
        return [
            NotificationReadModel(
                id=row.id,
                recipient_id=row.recipient_id,
                notification_type=row.notification_type,
                title=row.title,
                message=row.message,
                source_event_id=row.source_event_id,
                is_read=row.is_read,
                created_at=row.created_at,
                read_at=row.read_at,
            )
            for row in rows
        ]