from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ProcessedKafkaMessage:
    event_id: UUID
    topic: str
    partition: int
    offset: int
    consumer_group: str
    event_type: str
    id: UUID = field(default_factory=uuid4)
    processed_at: datetime = field(default_factory=lambda: datetime.now(UTC))