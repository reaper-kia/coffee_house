from typing import Protocol, TYPE_CHECKING

# Для аннотаций используем TYPE_CHECKING, чтобы избежать циклических импортов
if TYPE_CHECKING:
    from src.modules.users.application.ports.user_repository import UserRepository
    from src.modules.catalog.application.ports.menu_category_repository import (
        MenuCategoryRepository,
    )
    from src.modules.catalog.application.ports.menu_item_repository import (
        MenuItemRepository,
    )


class UnitOfWork(Protocol):
    """
    Интерфейс Unit of Work.
    Управляет транзакциями и предоставляет доступ к репозиториям.
    """

    # Репозитории
    users: "UserRepository"
    menu_categories: "MenuCategoryRepository"
    menu_items: "MenuItemRepository"

    async def __aenter__(self) -> "UnitOfWork":
        """Вход в контекстный менеджер (открытие транзакции)."""
        ...

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """Выход из контекстного менеджера (закрытие транзакции)."""
        ...

    async def commit(self) -> None:
        """Фиксация транзакции."""
        ...

    async def rollback(self) -> None:
        """Откат транзакции."""
        ...


class UnitOfWorkFactory(Protocol):
    """
    Фабрика Unit of Work.
    Создаёт новый экземпляр UoW для каждого запроса.
    """

    def __call__(self) -> UnitOfWork:
        ...