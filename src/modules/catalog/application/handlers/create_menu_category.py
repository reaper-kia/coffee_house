from src.modules.catalog.domain.entities import MenuCategory
from src.modules.catalog.domain.value_objects import CategoryTitle, Position
from src.shared.application.unit_of_work import UnitOfWorkFactory
from ..commands.create_menu_category import CreateMenuCategoryCommand

class CreateMenuCategoryHandler:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def handle(self, cmd: CreateMenuCategoryCommand) -> MenuCategory:
        category = MenuCategory.create(
            title=CategoryTitle(cmd.title),
            position=Position(cmd.position),
            is_active=cmd.is_active,
        )
        async with self.uow_factory() as uow:
            await uow.menu_categories.save(category)
            await uow.commit()
        return category