import asyncio
import logging

from src.modules.notifications.application.exceptions import InvalidIntegrationEvent, UnsupportedIntegrationEvent
from src.modules.notifications.application.handlers.handle_customer_request_event import HandleCustomerRequestEventHandler
from src.modules.notifications.application.services.customer_request_message_builder import CustomerRequestMessageBuilder
from src.modules.notifications.infra.sender import TelegramNotificationSender
from src.shared.api.dependencies import get_unit_of_work_factory
from src.shared.infra.kafka.consumer import KafkaConsumedMessage, KafkaEventConsumer
from src.shared.infra.kafka.dlq import create_dlq_key, create_dlq_payload
from src.shared.infra.kafka.producer import KafkaEventProducer
from src.core.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_to_dlq(
    *,
    dlq_producer: KafkaEventProducer,
    message: KafkaConsumedMessage,
    error: BaseException,
    attempts: int,
) -> None:
    dlq_key = create_dlq_key(message)
    dlq_payload = create_dlq_payload(
        message=message,
        error=error,
        attempts=attempts,
    )
    
    await dlq_producer.send_json(
        topic=settings.kafka_customer_request_events_dlq_topic,
        key=dlq_key,
        value=dlq_payload,
    )
    
async def process_message_with_retries(
    *,
    handler: HandleCustomerRequestEventHandler,
    dlq_producer: KafkaEventProducer,
    message: KafkaConsumedMessage,
) -> None:
    max_attempts = (
        settings.kafka_consumer_max_attempts
    )
    retry_delay_seconds = (
        settings.kafka_consumer_retry_delay_seconds
    )

    last_error: BaseException | None = None
    try:
        await handler.handle(message)
        return
    except (InvalidIntegrationEvent, UnsupportedIntegrationEvent) as exc:
        logger.warning(
            "Invalid or unsupported Kafka event. Sending to DLQ. "
            "topic=%s partition=%s offset=%s error=%s",
            message.topic,
            message.partition,
            message.offset,
            exc,
        )
        
        await send_to_dlq(
            dlq_producer=dlq_producer,
            message=message,
            error=exc,
            attempts=1,
        )
        return
    
    except Exception as exc:
        last_error = exc

        logger.warning(
            "Kafka message processing attempt failed. "
            "attempt=1/%s topic=%s partition=%s "
            "offset=%s error=%s",
            max_attempts,
            message.topic,
            message.partition,
            message.offset,
            exc,
        )
    
    for attempt in range(2, max_attempts + 1):
        try:
            await asyncio.sleep(retry_delay_seconds)
            
            await handler.handle(message)
            return
        except Exception as exc:
            last_error = exc
            
            logger.warning(
                "Kafka message processing attempt failed. "
                "attempt=%s/%s topic=%s partition=%s offset=%s error=%s",
                attempt,
                max_attempts,
                message.topic,
                message.partition,
                message.offset,
                exc,
            )
    
    if last_error is None:
        last_error = RuntimeError("Unknown Kafka message processing error")
        
    logger.error(
        "Kafka message processing failed after retries. Sending to DLQ. "
        "topic=%s partition=%s offset=%s error=%s",
        message.topic,
        message.partition,
        message.offset,
        last_error,
    )
    
    await send_to_dlq(
        dlq_producer=dlq_producer,
        message=message,
        error=last_error,
        attempts=max_attempts,
    )
    
async def main() -> None:
    consumer = KafkaEventConsumer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        client_id=f"{settings.kafka_client_id}-notifications-consumer",
        group_id=settings.kafka_notifications_consumer_group,
        topic=settings.kafka_customer_request_events_topic,
        auto_offset_reset="latest",
        enable_auto_commit=False,
    )
    
    dlq_producer = KafkaEventProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        client_id=f"{settings.kafka_client_id}-notifications-dlq-producer",
    )
    
    sender = TelegramNotificationSender(
        bot_token=settings.telegram_bot_token,
        timeout_seconds=settings.telegram_api_timeout_seconds,
    )
    
    handler = HandleCustomerRequestEventHandler(
        uow_factory=get_unit_of_work_factory(),
        sender=sender,
        message_builder=CustomerRequestMessageBuilder(),
        consumer_group=settings.kafka_notifications_consumer_group,
    )
    
    await consumer.start()
    await dlq_producer.start()
    
    logger.info("Customer request notifications consumer started")
    
    try:
        while True:
            message = await consumer.get_one()
            
            await process_message_with_retries(
                handler=handler,
                dlq_producer=dlq_producer,
                message=message,
            )
            
            await consumer.commit()
            
    finally:
        await consumer.stop()
        await dlq_producer.stop()
        
        logger.info("Customer request notifications consumer stopped")
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Customer request notifications consumer interrupted")