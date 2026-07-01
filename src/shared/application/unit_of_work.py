from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Импорты репозиториев из существующих модулей
from src.modules.users.infra.repositories import SQLAlchemyUserRepository
# Если у вас есть репозиторий для auth (например, для токенов/сессий), раскомментируйте и добавьте:
# from src.modules.auth.infra.repositories import SQLAlchemyAuthRepository

# Если у вас есть outbox, раскомментируйте:
# from src.shared.outbox.infra.repositories import SQLAlchemyOutboxRepository


class UnitOfWork(Protocol):
    users: SQLAlchemyUserRepository
    # auth_tokens: SQLAlchemyAuthRepository  # если есть
    # outbox: SQLAlchemyOutboxRepository     # если есть

    async def __aenter__(self) -> "UnitOfWork":
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...


class UnitOfWorkFactory(Protocol):
    def __call__(self) -> UnitOfWork:
        ...


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.users = SQLAlchemyUserRepository(self.session)
        # Если есть репозиторий auth – раскомментируйте:
        # self.auth_tokens = SQLAlchemyAuthRepository(self.session)
        # Если есть outbox – раскомментируйте:
        # self.outbox = SQLAlchemyOutboxRepository(self.session)
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