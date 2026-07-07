from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.modules.notifications.application.ports.notification_delivery_repository import NotificationDeliveryRepository
from src.modules.notifications.application.ports.processed_message_repository import ProcessedKafkaMessageRepository
from src.modules.notifications.domain.delivery import NotificationDelivery
from src.modules.notifications.domain.enums import NotificationChannel, NotificationDeliveryStatus
from src.modules.notifications.domain.processed_message import ProcessedKafkaMessage
from src.modules.notifications.infra.models import NotificationDeliveryModel, ProcessedKafkaMessageModel
from src.modules.notifications.domain.exceptions import NotificationNotFoundError



class SQLAlchemyNotificationDeliveryRepository(NotificationDeliveryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, notification: NotificationDelivery) -> NotificationDelivery:
        self.session.add(self._to_model(notification))
        
        return notification
        
    async def save(self, notification: NotificationDelivery) -> None:
        model = await self.session.get(NotificationDeliveryModel, notification.id)
        
        if model is None:
            raise NotificationNotFoundError("Notification not found.")
        
        self._apply_entity_to_model(notification, model)
    
    async def get_by_event_channel_recipient(self, *, event_id: UUID, channel: NotificationChannel, recipient: str) -> NotificationDelivery | None:
        stmt = select(NotificationDeliveryModel).where(
            NotificationDeliveryModel.event_id == event_id,
            NotificationDeliveryModel.channel == channel.value,
            NotificationDeliveryModel.recipient == recipient,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        return self._to_entity(model)
        
        


    
    @staticmethod
    def _to_model(delivery: NotificationDelivery) -> NotificationDeliveryModel:
        return NotificationDeliveryModel(
            id=delivery.id,
            event_id=delivery.event_id,
            customer_request_id=delivery.customer_request_id,
            channel=delivery.channel.value,
            recipient=delivery.recipient,
            message=delivery.message,
            status=delivery.status.value,
            attempts=delivery.attempts,
            last_error=delivery.last_error,
            sent_at=delivery.sent_at,
            created_at=delivery.created_at,
            updated_at=delivery.updated_at,
        )

    @staticmethod
    def _to_entity(model: NotificationDeliveryModel) -> NotificationDelivery:
        return NotificationDelivery(
            id=model.id,
            event_id=model.event_id,
            customer_request_id=model.customer_request_id,
            channel=NotificationChannel(model.channel),
            recipient=model.recipient,
            message=model.message,
            status=NotificationDeliveryStatus(model.status),
            attempts=model.attempts,
            last_error=model.last_error,
            sent_at=model.sent_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _apply_entity_to_model(
        delivery: NotificationDelivery,
        model: NotificationDeliveryModel,
    ) -> None:
        model.event_id = delivery.event_id
        model.customer_request_id = delivery.customer_request_id
        model.channel = delivery.channel.value
        model.recipient = delivery.recipient
        model.message = delivery.message
        model.status = delivery.status.value
        model.attempts = delivery.attempts
        model.last_error = delivery.last_error
        model.sent_at = delivery.sent_at
        model.created_at = delivery.created_at
        model.updated_at = delivery.updated_at
    
class SQLAlchemyProcessedKafkaMessageRepository(ProcessedKafkaMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add(self, message: ProcessedKafkaMessage) -> ProcessedKafkaMessage:
        self.session.add(self._to_model(message))
        
        return message

    async def exists(self, event_id: UUID) -> bool:
        stmt = select(ProcessedKafkaMessageModel).where(ProcessedKafkaMessageModel.event_id == event_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
        
        
    
    @staticmethod
    def _to_model(message: ProcessedKafkaMessage) -> ProcessedKafkaMessageModel:
        return ProcessedKafkaMessageModel(
            id=message.id,
            event_id=message.event_id,
            topic=message.topic,
            partition=message.partition,
            offset=message.offset,
            consumer_group=message.consumer_group,
            event_type=message.event_type,
            processed_at=message.processed_at,
        )