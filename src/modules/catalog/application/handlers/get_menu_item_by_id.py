from typing import Optional
from uuid import UUID
from src.modules.catalog.application.ports.menu_read_repositories import MenuItemReadRepository
from src.modules.catalog.application.read_models import MenuItemReadModel
from src.modules.catalog.domain.exceptions import MenuItemNotFoundError
from ..queries.get_menu_item import GetMenuItemQuery

class GetMenuItemByIdHandler:
    def __init__(self, read_repo: MenuItemReadRepository):
        self.read_repo = read_repo

    async def handle(self, query: GetMenuItemQuery) -> MenuItemReadModel:
        item = await self.read_repo.get_by_id(query.menu_item_id)
        if item is None:
            raise MenuItemNotFoundError(f"MenuItem {query.menu_item_id} not found")
        return item