from src.modules.catalog.application.ports.menu_item_repository import MenuItemRepository
from src.modules.catalog.domain.entities import MenuItem
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.modules.catalog.domain.exceptions import MenuItemNotFoundError
from ..commands.change_menu_item_availability import ChangeMenuItemAvailabilityCommand

class ChangeMenuItemAvailabilityHandler:
    def __init__(
        self,
        item_repo: MenuItemRepository,
        uow_factory: UnitOfWorkFactory,
    ):
        self.item_repo = item_repo
        self.uow_factory = uow_factory

    async def handle(self, cmd: ChangeMenuItemAvailabilityCommand) -> MenuItem:
        item = await self.item_repo.get_by_id(cmd.item_id)
        if item is None:
            raise MenuItemNotFoundError(f"MenuItem {cmd.item_id} not found")

        if cmd.is_available:
            item.mark_available()
        else:
            item.mark_unavailable()

        async with self.uow_factory() as uow:
            await self.item_repo.save(item)
            await uow.commit()
        return item