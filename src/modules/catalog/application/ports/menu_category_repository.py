from typing import Protocol, Optional, List
from uuid import UUID
from src.modules.catalog.domain.entities import MenuCategory

class MenuCategoryRepository(Protocol):
    async def save(self, category: MenuCategory) -> None:
        ...

    async def get_by_id(self, category_id: UUID) -> Optional[MenuCategory]:
        ...

    async def delete(self, category_id: UUID) -> None:
        ...

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[MenuCategory]:
        ...

    async def list_active(self, limit: int = 100, offset: int = 0) -> List[MenuCategory]:
        ...

    async def exists_by_id(self, category_id: UUID) -> bool:
        ...