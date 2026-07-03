from src.modules.catalog.application.ports.menu_category_repository import MenuCategoryRepository
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.modules.catalog.domain.entities import MenuCategory
from ..commands.create_menu_category import CreateMenuCategoryCommand

class CreateMenuCategoryHandler:
    def __init__(
        self,
        repo: MenuCategoryRepository,
        uow_factory: UnitOfWorkFactory,
    ):
        self.repo = repo
        self.uow_factory = uow_factory

    async def handle(self, cmd: CreateMenuCategoryCommand) -> MenuCategory:
        category = MenuCategory.create(
            title=cmd.title,
            position=cmd.position,
            is_active=cmd.is_active,
        )
        async with self.uow_factory() as uow:
            await self.repo.save(category)
            await uow.commit()
        return category