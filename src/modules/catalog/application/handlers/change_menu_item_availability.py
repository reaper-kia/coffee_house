from src.modules.catalog.domain.entities import MenuItem
from src.modules.catalog.domain.exceptions import MenuItemNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory
from ..commands.change_menu_item_availability import ChangeMenuItemAvailabilityCommand

class ChangeMenuItemAvailabilityHandler:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def handle(self, cmd: ChangeMenuItemAvailabilityCommand) -> MenuItem:
        async with self.uow_factory() as uow:
            item = await uow.menu_items.get_by_id(cmd.item_id)
            if item is None:
                raise MenuItemNotFoundError(f"MenuItem {cmd.item_id} not found")

            if cmd.is_available:
                item.mark_available()
            else:
                item.mark_unavailable()

            await uow.menu_items.save(item)
            await uow.commit()
        return item