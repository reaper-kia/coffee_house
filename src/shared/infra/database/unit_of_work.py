from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.users.infra.repositories import SQLAlchemyUserRepository
from src.modules.catalog.infra.repositories import (
    SQLAlchemyMenuCategoryRepository,
    SQLAlchemyMenuItemRepository,
)
from src.shared.application.unit_of_work import UnitOfWork
from src.modules.customer_requests.infra.repositories import SQLAlchemyCustomerRequestRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.users = SQLAlchemyUserRepository(self.session)
        self.menu_categories = SQLAlchemyMenuCategoryRepository(self.session)
        self.menu_items = SQLAlchemyMenuItemRepository(self.session)
        self.customer_requests = SQLAlchemyCustomerRequestRepository(self.session)
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