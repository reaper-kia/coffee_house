# src/modules/catalog/api/dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infra.database.session import get_async_session
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.shared.api.dependencies import get_unit_of_work_factory
from src.shared.application.mediator import Mediator

# ----- Репозитории (infra) -----
from src.modules.catalog.infra.repositories import (
    SQLAlchemyMenuCategoryRepository,
    SQLAlchemyMenuItemRepository,
    SQLAlchemyMenuCategoryReadRepository,
    SQLAlchemyMenuItemReadRepository,
)

# ----- Порты (write) -----
from src.modules.catalog.application.ports.menu_category_repository import (
    MenuCategoryRepository,
)
from src.modules.catalog.application.ports.menu_item_repository import (
    MenuItemRepository,
)

# ----- Порты (read) -----
from src.modules.catalog.application.ports.menu_read_repositories import (
    MenuCategoryReadRepository,
    MenuItemReadRepository,
)

# ----- Команды -----
from src.modules.catalog.application.commands.create_menu_category import (
    CreateMenuCategoryCommand,
)
from src.modules.catalog.application.commands.update_menu_category import (
    UpdateMenuCategoryCommand,
)
from src.modules.catalog.application.commands.delete_menu_category import (
    DeleteMenuCategoryCommand,
)
from src.modules.catalog.application.commands.create_menu_item import (
    CreateMenuItemCommand,
)
from src.modules.catalog.application.commands.update_menu_item import (
    UpdateMenuItemCommand,
)
from src.modules.catalog.application.commands.delete_menu_item import (
    DeleteMenuItemCommand,
)
from src.modules.catalog.application.commands.change_menu_item_availability import (
    ChangeMenuItemAvailabilityCommand,
)

# ----- Хендлеры (команды) -----
from src.modules.catalog.application.handlers.create_menu_category import (
    CreateMenuCategoryHandler,
)
from src.modules.catalog.application.handlers.update_menu_category import (
    UpdateMenuCategoryHandler,
)
from src.modules.catalog.application.handlers.delete_menu_category import (
    DeleteMenuCategoryHandler,
)
from src.modules.catalog.application.handlers.create_menu_item import (
    CreateMenuItemHandler,
)
from src.modules.catalog.application.handlers.update_menu_item import (
    UpdateMenuItemHandler,
)
from src.modules.catalog.application.handlers.delete_menu_item import (
    DeleteMenuItemHandler,
)
from src.modules.catalog.application.handlers.change_menu_item_availability import (
    ChangeMenuItemAvailabilityHandler,
)

# ----- Запросы (queries) -----
from src.modules.catalog.application.queries.get_categories import (
    GetCategoriesQuery,
)
from src.modules.catalog.application.queries.get_menu_items import (
    GetMenuItemsQuery,
)
from src.modules.catalog.application.queries.get_menu_item import (
    GetMenuItemQuery,
)

# ----- Хендлеры (запросы) -----
from src.modules.catalog.application.handlers.list_categories import (
    ListCategoriesHandler,
)
from src.modules.catalog.application.handlers.list_menu_items import (
    ListMenuItemsHandler,
)
from src.modules.catalog.application.handlers.get_menu_item_by_id import (
    GetMenuItemByIdHandler,
)


# ============================================================================
# 1. Фабрики write-репозиториев
# ============================================================================

async def get_menu_category_repository(
    session: AsyncSession = Depends(get_async_session),
) -> MenuCategoryRepository:
    return SQLAlchemyMenuCategoryRepository(session)

async def get_menu_item_repository(
    session: AsyncSession = Depends(get_async_session),
) -> MenuItemRepository:
    return SQLAlchemyMenuItemRepository(session)


# ============================================================================
# 2. Фабрики read-репозиториев
# ============================================================================

async def get_menu_category_read_repository(
    session: AsyncSession = Depends(get_async_session),
) -> MenuCategoryReadRepository:
    return SQLAlchemyMenuCategoryReadRepository(session)

async def get_menu_item_read_repository(
    session: AsyncSession = Depends(get_async_session),
) -> MenuItemReadRepository:
    return SQLAlchemyMenuItemReadRepository(session)


# ============================================================================
# 3. Фабрики командных хендлеров (write) – только UoW
# ============================================================================

async def get_create_menu_category_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> CreateMenuCategoryHandler:
    return CreateMenuCategoryHandler(uow_factory)

async def get_update_menu_category_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> UpdateMenuCategoryHandler:
    return UpdateMenuCategoryHandler(uow_factory)

async def get_delete_menu_category_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> DeleteMenuCategoryHandler:
    return DeleteMenuCategoryHandler(uow_factory)

async def get_create_menu_item_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> CreateMenuItemHandler:
    return CreateMenuItemHandler(uow_factory)

async def get_update_menu_item_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> UpdateMenuItemHandler:
    return UpdateMenuItemHandler(uow_factory)

async def get_delete_menu_item_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> DeleteMenuItemHandler:
    return DeleteMenuItemHandler(uow_factory)

async def get_change_menu_item_availability_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> ChangeMenuItemAvailabilityHandler:
    return ChangeMenuItemAvailabilityHandler(uow_factory)


# ============================================================================
# 4. Фабрики query-хендлеров (чтение)
# ============================================================================

async def get_list_categories_handler(
    read_repo: MenuCategoryReadRepository = Depends(get_menu_category_read_repository),
) -> ListCategoriesHandler:
    return ListCategoriesHandler(read_repo)

async def get_list_menu_items_handler(
    read_repo: MenuItemReadRepository = Depends(get_menu_item_read_repository),
) -> ListMenuItemsHandler:
    return ListMenuItemsHandler(read_repo)

async def get_get_menu_item_by_id_handler(
    read_repo: MenuItemReadRepository = Depends(get_menu_item_read_repository),
) -> GetMenuItemByIdHandler:
    return GetMenuItemByIdHandler(read_repo)


# ============================================================================
# 5. Медиатор (регистрация всех команд и запросов)
# ============================================================================

async def get_catalog_mediator(
    create_menu_category_handler: CreateMenuCategoryHandler = Depends(get_create_menu_category_handler),
    update_menu_category_handler: UpdateMenuCategoryHandler = Depends(get_update_menu_category_handler),
    delete_menu_category_handler: DeleteMenuCategoryHandler = Depends(get_delete_menu_category_handler),
    create_menu_item_handler: CreateMenuItemHandler = Depends(get_create_menu_item_handler),
    update_menu_item_handler: UpdateMenuItemHandler = Depends(get_update_menu_item_handler),
    delete_menu_item_handler: DeleteMenuItemHandler = Depends(get_delete_menu_item_handler),
    change_availability_handler: ChangeMenuItemAvailabilityHandler = Depends(get_change_menu_item_availability_handler),
    list_categories_handler: ListCategoriesHandler = Depends(get_list_categories_handler),
    list_menu_items_handler: ListMenuItemsHandler = Depends(get_list_menu_items_handler),
    get_menu_item_by_id_handler: GetMenuItemByIdHandler = Depends(get_get_menu_item_by_id_handler),
) -> Mediator:
    mediator = Mediator()

    # Регистрация команд (write)
    mediator.register(CreateMenuCategoryCommand, create_menu_category_handler)
    mediator.register(UpdateMenuCategoryCommand, update_menu_category_handler)
    mediator.register(DeleteMenuCategoryCommand, delete_menu_category_handler)
    mediator.register(CreateMenuItemCommand, create_menu_item_handler)
    mediator.register(UpdateMenuItemCommand, update_menu_item_handler)
    mediator.register(DeleteMenuItemCommand, delete_menu_item_handler)
    mediator.register(ChangeMenuItemAvailabilityCommand, change_availability_handler)

    # Регистрация запросов (read)
    mediator.register(GetCategoriesQuery, list_categories_handler)
    mediator.register(GetMenuItemsQuery, list_menu_items_handler)
    mediator.register(GetMenuItemQuery, get_menu_item_by_id_handler)

    return mediator