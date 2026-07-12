from src.modules.catalog.domain.entities import MenuItem
from src.modules.catalog.domain.value_objects import ProductTitle, Description, Position
from src.modules.catalog.domain.exceptions import MenuItemNotFoundError, CategoryNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory
from ..commands.update_menu_item import UpdateMenuItemCommand
from src.shared.domain.value_objects import Money

class UpdateMenuItemHandler:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def handle(self, cmd: UpdateMenuItemCommand) -> MenuItem:
        async with self.uow_factory() as uow:
            item = await uow.menu_items.get_by_id(cmd.item_id)
            if item is None:
                raise MenuItemNotFoundError(f"MenuItem {cmd.item_id} not found")

            if cmd.category_id is not None:
                exists = await uow.menu_categories.exists_by_id(cmd.category_id)
                if not exists:
                    raise CategoryNotFoundError(f"Category {cmd.category_id} not found")
                item.assign_category(cmd.category_id)

            if cmd.title is not None:
                item.change_title(ProductTitle(cmd.title))
            if cmd.description is not None:
                item.change_description(Description(cmd.description))
            if cmd.price_amount is not None and cmd.price_currency is not None:
                item.change_price(Money(cmd.price_amount, cmd.price_currency))
            if cmd.image_url is not None:
                item.change_image_url(cmd.image_url)
            if cmd.is_available is not None:
                if cmd.is_available:
                    item.mark_available()
                else:
                    item.mark_unavailable()
            if cmd.position is not None:
                item.change_position(Position(cmd.position))

            await uow.menu_items.save(item)
            await uow.commit()
        return item