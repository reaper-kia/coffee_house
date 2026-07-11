from src.modules.catalog.domain.entities import MenuCategory
from src.modules.catalog.domain.value_objects import CategoryTitle, Position
from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory
from ..commands.update_menu_category import UpdateMenuCategoryCommand

class UpdateMenuCategoryHandler:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def handle(self, cmd: UpdateMenuCategoryCommand) -> MenuCategory:
        async with self.uow_factory() as uow:
            category = await uow.menu_categories.get_by_id(cmd.category_id)
            if category is None:
                raise CategoryNotFoundError(f"Category {cmd.category_id} not found")

            if cmd.title is not None:
                category.change_title(CategoryTitle(cmd.title))
            if cmd.position is not None:
                category.change_position(Position(cmd.position))
            if cmd.is_active is not None:
                if cmd.is_active:
                    category.activate()
                else:
                    category.deactivate()

            await uow.menu_categories.save(category)
            await uow.commit()
        return category