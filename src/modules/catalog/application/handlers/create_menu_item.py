from src.modules.catalog.domain.entities import MenuItem
from src.modules.catalog.domain.value_objects import ProductTitle, Description, Position
from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory
from ..commands.create_menu_item import CreateMenuItemCommand
from src.shared.domain.value_objects import Money

class CreateMenuItemHandler:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def handle(self, cmd: CreateMenuItemCommand) -> MenuItem:
        # Проверка существования категории (если указана)
        if cmd.category_id is not None:
            async with self.uow_factory() as uow:
                exists = await uow.menu_categories.exists_by_id(cmd.category_id)
                if not exists:
                    raise CategoryNotFoundError(f"Category {cmd.category_id} not found")
        # Создание сущности (можно вне UoW, т.к. она ещё не сохранена)
        item = MenuItem.create(
            title=ProductTitle(cmd.title),
            price=Money(cmd.price_amount, cmd.price_currency),
            description=Description(cmd.description),
            is_available=cmd.is_available,
            category_id=cmd.category_id,
            image_url=cmd.image_url,
            position=Position(cmd.position),
        )

        async with self.uow_factory() as uow:
            await uow.menu_items.save(item)
            await uow.commit()
        return item