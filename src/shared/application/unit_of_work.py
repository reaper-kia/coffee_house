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
    # ---------- ИЗМЕНЕНИЕ 1: Замена OrderRepository на CustomerRequestRepository ----------
    from src.modules.customer_requests.application.ports.customer_request_repository import (
        CustomerRequestRepository,
    )
    # ---------- ИЗМЕНЕНИЕ 2: Добавление репозитория для снапшотов ----------
    from src.modules.customer_requests.application.ports.menu_item_snapshot_repository import (
        MenuItemSnapshotRepository,
    )


class UnitOfWork(Protocol):
    """
    Интерфейс Unit of Work.
    Управляет транзакциями и предоставляет доступ к репозиториям.
    """

    # Репозитории (существующие)
    users: "UserRepository"
    menu_categories: "MenuCategoryRepository"
    menu_items: "MenuItemRepository"

    # ---------- ИЗМЕНЕНИЕ 3: Вместо orders теперь customer_requests ----------
    customer_requests: "CustomerRequestRepository"

    # ---------- ИЗМЕНЕНИЕ 4: Добавлен репозиторий для снапшотов ----------
    menu_item_snapshots: "MenuItemSnapshotRepository"

    # Outbox и другие репозитории (если они уже есть в протоколе) остаются без изменений

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