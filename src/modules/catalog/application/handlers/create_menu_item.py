from src.modules.catalog.application.ports.menu_category_repository import MenuCategoryRepository
from src.modules.catalog.application.ports.menu_item_repository import MenuItemRepository
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.modules.catalog.domain.entities import MenuItem
from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from ..commands.create_menu_item import CreateMenuItemCommand

class CreateMenuItemHandler:
    def __init__(
        self,
        item_repo: MenuItemRepository,
        category_repo: MenuCategoryRepository,
        uow_factory: UnitOfWorkFactory,
    ):
        self.item_repo = item_repo
        self.category_repo = category_repo
        self.uow_factory = uow_factory

    async def handle(self, cmd: CreateMenuItemCommand) -> MenuItem:
        if cmd.category_id is not None:
            exists = await self.category_repo.exists_by_id(cmd.category_id)
            if not exists:
                raise CategoryNotFoundError(f"Category {cmd.category_id} not found")

        item = MenuItem.create(
            title=cmd.title,
            price=cmd.price,
            description=cmd.description,
            is_available=cmd.is_available,
            category_id=cmd.category_id,
            image_url=cmd.image_url,
            position=cmd.position,
        )

        async with self.uow_factory() as uow:
            await self.item_repo.save(item)
            await uow.commit()
        return item