from typing import List
from src.modules.catalog.application.ports.menu_read_repositories import MenuCategoryReadRepository
from src.modules.catalog.application.read_models import CategoryReadModel
from ..queries.get_categories import GetCategoriesQuery

class ListCategoriesHandler:
    def __init__(self, read_repo: MenuCategoryReadRepository):
        self.read_repo = read_repo

    async def handle(self, query: GetCategoriesQuery) -> List[CategoryReadModel]:
        return await self.read_repo.list_categories(
            active_only=query.active_only,
            limit=query.limit,
            offset=query.offset,
        )