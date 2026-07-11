from src.modules.catalog.domain.exceptions import MenuItemNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory
from ..commands.delete_menu_item import DeleteMenuItemCommand

class DeleteMenuItemHandler:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def handle(self, cmd: DeleteMenuItemCommand):
        async with self.uow_factory() as uow:
            item = await uow.menu_items.get_by_id(cmd.item_id)
            if item is None:
                raise MenuItemNotFoundError(f"MenuItem {cmd.item_id} not found")

            await uow.menu_items.delete(cmd.item_id)
            await uow.commit()