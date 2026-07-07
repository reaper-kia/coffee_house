from typing import Protocol
from uuid import UUID

from src.modules.notifications.domain.processed_message import ProcessedKafkaMessage


class ProcessedKafkaMessageRepository(Protocol):
    async def exists(self, event_id: UUID) -> bool:
        ...

    async def add(self, message: ProcessedKafkaMessage) -> ProcessedKafkaMessage:
        ...