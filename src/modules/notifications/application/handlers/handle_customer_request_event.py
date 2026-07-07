from dataclasses import dataclass
from typing import Any
from uuid import UUID


from src.modules.notifications.application.exceptions import InvalidIntegrationEvent, UnsupportedIntegrationEvent
from src.modules.notifications.domain.delivery import NotificationDelivery
from src.modules.notifications.domain.enums import NotificationChannel
from src.modules.notifications.domain.processed_message import ProcessedKafkaMessage
from src.shared.events.customer_request_event import CUSTOMER_REQUEST_AGGREGATE
from src.modules.notifications.application.ports.notification_sender import NotificationSender
from src.modules.notifications.application.services.customer_request_message_builder import CustomerRequestMessageBuilder
from src.shared.infra.kafka.consumer import KafkaConsumedMessage
from src.shared.application.unit_of_work import UnitOfWorkFactory

@dataclass(slots=True)
class HandleCustomerRequestEventHandler:
    uow_factory: UnitOfWorkFactory
    sender: NotificationSender
    message_builder: CustomerRequestMessageBuilder
    consumer_group: str    
    
    async def handle(self, message: KafkaConsumedMessage) -> None:
        event = self._validate_event(message.value)
        
        event_id = UUID(str(event["event_id"]))
        event_type = str(event["event_type"])
        
        payload = event["payload"]
        
        async with self.uow_factory() as uow:
            already_processed = await uow.processed_kafka_messages.exists(
                event_id,
            )
            if already_processed:
                return
            
        notification_message = self.message_builder.build(event=event)
            
        if notification_message is None:
            await self._mark_processed(
                message=message,
                event_id=event_id,
                event_type=event_type,
            )
            return
        
        recipient = self._get_recipient(payload)
        customer_request_id = UUID(str(payload["customer_request_id"]))
        
        async with self.uow_factory() as uow:
            existing_delivery = (
                await uow.notification_deliveries.get_by_event_channel_recipient(
                    event_id=event_id,
                    channel=NotificationChannel.TELEGRAM,
                    recipient=recipient,
                )
            )
            if existing_delivery is None:
                delivery = NotificationDelivery(
                    event_id=event_id,
                    channel=NotificationChannel.TELEGRAM,
                    recipient=recipient,
                    message=notification_message,
                    customer_request_id=customer_request_id,
                )
                await uow.notification_deliveries.add(delivery)
            await uow.commit()
                
        try:
            await self.sender.send(
                recipient=recipient,
                message=notification_message,
            )
        except Exception as exc:
            async with self.uow_factory() as uow:
                delivery = (
                    await uow.notification_deliveries.get_by_event_channel_recipient(
                        event_id=event_id,
                        channel=NotificationChannel.TELEGRAM,
                        recipient=recipient,
                    )
                )
                if delivery is not None:
                    delivery.mark_failed(error=str(exc))
                    await uow.notification_deliveries.save(delivery)
                
                await uow.commit()
            
            raise
        
        async with self.uow_factory() as uow:
            delivery = (
                    await uow.notification_deliveries.get_by_event_channel_recipient(
                        event_id=event_id,
                        channel=NotificationChannel.TELEGRAM,
                        recipient=recipient,
                    )
                )
            
            if delivery is not None:
                delivery.mark_sent()
                await uow.notification_deliveries.save(delivery)
            
            processed_message = ProcessedKafkaMessage(
                event_id=event_id,
                topic=message.topic,
                partition=message.partition,
                offset=message.offset,
                consumer_group=self.consumer_group,
                event_type=event_type,
            )
            
            await uow.processed_kafka_messages.add(processed_message)
            await uow.commit()
                    
    async def _mark_processed(
        self,
        *,
        message: KafkaConsumedMessage,
        event_id: UUID,
        event_type: str,
    ) -> None:
        async with self.uow_factory() as uow:
            processed_message = ProcessedKafkaMessage(
                event_id=event_id,
                topic=message.topic,
                partition=message.partition,
                offset=message.offset,
                consumer_group=self.consumer_group,
                event_type=event_type,
            )
            
            await uow.processed_kafka_messages.add(processed_message)
            await uow.commit()
    
    def _validate_event(self, event: dict[str, Any]) -> dict[str, Any]:
        required_fields = {
            "event_id",
            "event_type",
            "event_version",
            "aggregate_type",
            "aggregate_id",
            "payload",
        }
        missing_fields = required_fields - event.keys()
        
        if missing_fields:
            raise InvalidIntegrationEvent(
                f"Missing required event fields: {sorted(missing_fields)}",
            )
        
        if event["event_version"] != 1:
            raise UnsupportedIntegrationEvent(
                f"Unsupported event_version: {event['event_version']}",
            )
        
        if event["aggregate_type"] != CUSTOMER_REQUEST_AGGREGATE:
            raise UnsupportedIntegrationEvent(
                f"Unsupported aggregate_type: {event['aggregate_type']}",
            )
        
        payload = event["payload"]
        if not isinstance(payload, dict):
            raise InvalidIntegrationEvent("Event payload must be object")

        if "customer_request_id" not in payload:
            raise InvalidIntegrationEvent(
                "payload.customer_request_id is required",
            )
        
        return event

    def _get_recipient(self, payload: dict[str, Any]) -> str:
        recipient = payload.get("customer_telegram_chat_id")
        if not recipient:
            raise InvalidIntegrationEvent(
                "payload.customer_telegram_chat_id is required",
            )
        return str(recipient)