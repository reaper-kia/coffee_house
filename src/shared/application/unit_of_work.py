from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


from src.shared.outbox.application.repositories import OutboxRepository
from src.modules.users.application.ports.user_repository import UserRepository



class UnitOfWork(Protocol):
    users: UserRepository
    outbox: OutboxRepository

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