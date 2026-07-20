from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from src.modules.customer_requests.application.read_models import (
    CustomerRequestReadModel,
    CustomerRequestPageReadModel,
)
from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType


class CustomerRequestReadRepository(ABC):
    """Порт для чтения read-моделей заявок."""

    @abstractmethod
    async def get_by_id(self, request_id: UUID) -> Optional[CustomerRequestReadModel]:
        """Вернуть read-модель по ID."""
        pass

    @abstractmethod
    async def list(
        self,
        status: Optional[CustomerRequestStatus],
        request_type: Optional[CustomerRequestType],
        limit: int,
        offset: int,
    ) -> CustomerRequestPageReadModel:
        """Вернуть страницу read-моделей с общим количеством."""
        pass