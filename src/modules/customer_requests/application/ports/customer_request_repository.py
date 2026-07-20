from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from src.modules.customer_requests.domain.entities import CustomerRequest


class CustomerRequestRepository(ABC):
    """Порт для сохранения и загрузки агрегата CustomerRequest."""

    @abstractmethod
    async def add(self, request: CustomerRequest) -> None:
        """Сохранить новый агрегат (вставка)."""
        pass

    @abstractmethod
    async def get_by_id(self, request_id: UUID) -> Optional[CustomerRequest]:
        """Найти заявку по ID, вернуть агрегат или None."""
        pass

    @abstractmethod
    async def save(self, request: CustomerRequest) -> None:
        """Обновить существующий агрегат."""
        pass