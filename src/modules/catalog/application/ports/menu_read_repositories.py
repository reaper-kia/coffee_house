from typing import Protocol, List, Optional
from uuid import UUID
from src.modules.catalog.application.read_models import CategoryReadModel, MenuItemReadModel

class MenuCategoryReadRepository(Protocol):
    async def list_categories(
        self,
        active_only: bool = True,
        limit: int = 100,
        offset: int = 0,
    ) -> List[CategoryReadModel]:
        ...

class MenuItemReadRepository(Protocol):
    async def list_menu_items(
        self,
        category_id: UUID | None = None,
        available_only: bool = True,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[MenuItemReadModel]:
        ...

    async def get_by_id(self, menu_item_id: UUID) -> Optional[MenuItemReadModel]:
        ...