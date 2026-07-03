from src.modules.catalog.application.ports.menu_category_repository import MenuCategoryRepository
from src.modules.catalog.domain.entities import MenuCategory
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from ..commands.update_menu_category import UpdateMenuCategoryCommand

class UpdateMenuCategoryHandler:
    def __init__(
        self,
        repo: MenuCategoryRepository,
        uow_factory: UnitOfWorkFactory,
    ):
        self.repo = repo
        self.uow_factory = uow_factory

    async def handle(self, cmd: UpdateMenuCategoryCommand) -> MenuCategory:
        category = await self.repo.get_by_id(cmd.category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category {cmd.category_id} not found")

        if cmd.title is not None:
            category.change_title(cmd.title)
        if cmd.position is not None:
            category.change_position(cmd.position)
        if cmd.is_active is not None:
            if cmd.is_active:
                category.activate()
            else:
                category.deactivate()

        async with self.uow_factory() as uow:
            await self.repo.save(category)
            await uow.commit()
        return category