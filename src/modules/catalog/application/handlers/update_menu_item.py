# application/handlers/update_menu_item.py
from src.modules.catalog.application.ports.menu_read_repositories import MenuItemReadRepository, MenuCategoryReadRepository
from src.modules.catalog.domain.entities import MenuItem
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.modules.catalog.domain.exceptions import MenuItemNotFoundError, CategoryNotFoundError
from ..commands.update_menu_item import UpdateMenuItemCommand

class UpdateMenuItemHandler:
    def __init__(
        self,
        item_repo: MenuItemReadRepository,
        category_repo: MenuCategoryReadRepository,
        uow_factory: UnitOfWorkFactory,
    ):
        self.item_repo = item_repo
        self.category_repo = category_repo
        self.uow_factory = uow_factory

    async def handle(self, cmd: UpdateMenuItemCommand) -> MenuItem:
        item = await self.item_repo.get_by_id(cmd.item_id)
        if item is None:
            raise MenuItemNotFoundError(f"MenuItem {cmd.item_id} not found")

        # Проверяем категорию, если она передана
        if cmd.category_id is not None:
            category_exists = await self.category_repo.exists_by_id(cmd.category_id)
            if not category_exists:
                raise CategoryNotFoundError(f"Category {cmd.category_id} not found")
            item.assign_category(cmd.category_id)

        # Применяем изменения
        if cmd.title is not None:
            item.change_title(cmd.title)
        if cmd.price is not None:
            item.change_price(cmd.price)
        if cmd.description is not None:
            item.change_description(cmd.description)
        if cmd.image_url is not None:
            item.change_image_url(cmd.image_url)
        if cmd.is_available is not None:
            if cmd.is_available:
                item.mark_available()
            else:
                item.mark_unavailable()
        if cmd.position is not None:
            item.change_position(cmd.position)

        async with self.uow_factory() as uow:
            await self.item_repo.save(item)
            await uow.commit()

        return item