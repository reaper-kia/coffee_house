from src.modules.catalog.application.ports.menu_category_repository import MenuCategoryRepository
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from ..commands.delete_menu_category import DeleteMenuCategoryCommand

class DeleteMenuCategoryHandler:
    def __init__(
        self,
        repo: MenuCategoryRepository,
        uow_factory: UnitOfWorkFactory,
    ):
        self.repo = repo
        self.uow_factory = uow_factory

    async def handle(self, cmd: DeleteMenuCategoryCommand):
        category = await self.repo.get_by_id(cmd.category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category {cmd.category_id} not found")

        async with self.uow_factory() as uow:
            await self.repo.delete(cmd.category_id)
            await uow.commit()