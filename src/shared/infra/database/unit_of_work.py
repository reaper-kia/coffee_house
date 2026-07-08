from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.notifications.infra.repositories import SQLAlchemyNotificationDeliveryRepository, SQLAlchemyProcessedKafkaMessageRepository
from src.shared.outbox.infra.repositories import SQLAlchemyOutboxRepository
from src.modules.users.infra.repositories import SQLAlchemyUserRepository
from src.shared.application.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.users = SQLAlchemyUserRepository(self.session)
        self.outbox = SQLAlchemyOutboxRepository(self.session)
        self.notification_deliveries = SQLAlchemyNotificationDeliveryRepository(self.session)
        self.processed_kafka_messages = SQLAlchemyProcessedKafkaMessageRepository(self.session)
        
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()