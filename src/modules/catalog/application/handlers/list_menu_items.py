from typing import List
from src.modules.catalog.application.ports.menu_read_repositories import MenuItemReadRepository
from src.modules.catalog.application.read_models import MenuItemReadModel
from ..queries.get_menu_items import GetMenuItemsQuery

class ListMenuItemsHandler:
    def __init__(self, read_repo: MenuItemReadRepository):
        self.read_repo = read_repo

    async def handle(self, query: GetMenuItemsQuery) -> List[MenuItemReadModel]:
        return await self.read_repo.list_menu_items(
            category_id=query.category_id,
            available_only=query.available_only,
            search=query.search,
            limit=query.limit,
            offset=query.offset,
        )