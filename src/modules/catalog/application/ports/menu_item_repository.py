from typing import Protocol, Optional, List
from uuid import UUID
from src.modules.catalog.domain.entities import MenuItem

class MenuItemRepository(Protocol):
    async def save(self, item: MenuItem) -> None:
        ...

    async def get_by_id(self, item_id: UUID) -> Optional[MenuItem]:
        ...

    async def delete(self, item_id: UUID) -> None:
        ...

    async def list_by_category(self, category_id: UUID, limit: int = 100, offset: int = 0) -> List[MenuItem]:
        ...

    async def list_available(self, limit: int = 100, offset: int = 0) -> List[MenuItem]:
        ...

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[MenuItem]:
        ...

    async def exists_by_id(self, item_id: UUID) -> bool:
        ...