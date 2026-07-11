from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory
from ..commands.delete_menu_category import DeleteMenuCategoryCommand

class DeleteMenuCategoryHandler:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def handle(self, cmd: DeleteMenuCategoryCommand):
        async with self.uow_factory() as uow:
            category = await uow.menu_categories.get_by_id(cmd.category_id)
            if category is None:
                raise CategoryNotFoundError(f"Category {cmd.category_id} not found")

            await uow.menu_categories.delete(cmd.category_id)
            await uow.commit()