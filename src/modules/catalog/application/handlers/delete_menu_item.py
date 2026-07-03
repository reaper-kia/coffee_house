# application/handlers/delete_menu_item.py
from src.modules.catalog.application.ports.menu_read_repositories import MenuItemReadRepository
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.modules.catalog.domain.exceptions import MenuItemNotFoundError
from ..commands.delete_menu_item import DeleteMenuItemCommand

class DeleteMenuItemHandler:
    def __init__(
        self,
        item_repo: MenuItemReadRepository,
        uow_factory: UnitOfWorkFactory,
    ):
        self.item_repo = item_repo
        self.uow_factory = uow_factory

    async def handle(self, cmd: DeleteMenuItemCommand):
        item = await self.item_repo.get_by_id(cmd.item_id)
        if item is None:
            raise MenuItemNotFoundError(f"MenuItem {cmd.item_id} not found")

        async with self.uow_factory() as uow:
            await self.item_repo.delete(cmd.item_id)
            await uow.commit()