from abc import ABC, abstractmethod
from uuid import UUID
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ProductSnapshot:
    menu_item_id: UUID
    title: str
    price_amount: Decimal
    price_currency: str


class MenuItemSnapshotRepository(ABC):
    """Порт для получения снапшотов товаров из каталога."""

    @abstractmethod
    async def get_available_by_ids(self, menu_item_ids: set[UUID]) -> dict[UUID, ProductSnapshot]:
        """Вернуть словарь {menu_item_id: ProductSnapshot} для доступных товаров."""
        pass