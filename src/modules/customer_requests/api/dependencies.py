# src/modules/customer_requests/api/dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infra.database.session import get_async_session
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.shared.api.dependencies import get_unit_of_work_factory
from src.shared.application.mediator import Mediator

# ----- Репозитории (infra) -----
from src.modules.customer_requests.infra.repositories import (
    SQLAlchemyCustomerRequestRepository,
    SQLAlchemyCustomerRequestReadRepository,
    SQLAlchemyMenuItemSnapshotRepository,
)

# ----- Порты (write) -----
from src.modules.customer_requests.application.ports.customer_request_repository import (
    CustomerRequestRepository,
)
from src.modules.customer_requests.application.ports.menu_item_snapshot_repository import (
    MenuItemSnapshotRepository,
)

# ----- Порты (read) -----
from src.modules.customer_requests.application.ports.customer_request_read_repository import (
    CustomerRequestReadRepository,
)

# ----- Команды -----
from src.modules.customer_requests.application.commands.create_customer_request import (
    CreateCustomerRequestCommand,
)
from src.modules.customer_requests.application.commands.change_customer_request_status import (
    ChangeCustomerRequestStatusCommand,
)

# ----- Запросы -----
from src.modules.customer_requests.application.queries.list_customer_requests import (
    ListCustomerRequestsQuery,
)
from src.modules.customer_requests.application.queries.get_customer_request import (
    GetCustomerRequestByIdQuery,
)

# ----- Хендлеры (команды) -----
from src.modules.customer_requests.application.handlers.create_customer_request import (
    CreateCustomerRequestHandler,
)
from src.modules.customer_requests.application.handlers.change_customer_request_status import (
    ChangeCustomerRequestStatusHandler,
)

# ----- Хендлеры (запросы) -----
from src.modules.customer_requests.application.handlers.list_customer_requests import (
    ListCustomerRequestsHandler,
)
from src.modules.customer_requests.application.handlers.get_customer_request_by_id import (
    GetCustomerRequestByIdHandler,
)


# ============================================================================
# 1. Фабрики write-репозиториев
# ============================================================================

async def get_customer_request_repository(
    session: AsyncSession = Depends(get_async_session),
) -> CustomerRequestRepository:
    return SQLAlchemyCustomerRequestRepository(session)

async def get_menu_item_snapshot_repository(
    session: AsyncSession = Depends(get_async_session),
) -> MenuItemSnapshotRepository:
    return SQLAlchemyMenuItemSnapshotRepository(session)


# ============================================================================
# 2. Фабрика read-репозитория
# ============================================================================

async def get_customer_request_read_repository(
    session: AsyncSession = Depends(get_async_session),
) -> CustomerRequestReadRepository:
    return SQLAlchemyCustomerRequestReadRepository(session)


# ============================================================================
# 3. Фабрики командных хендлеров (write) – используют UoW
# ============================================================================

async def get_create_customer_request_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> CreateCustomerRequestHandler:
    return CreateCustomerRequestHandler(uow_factory)

async def get_change_customer_request_status_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
) -> ChangeCustomerRequestStatusHandler:
    return ChangeCustomerRequestStatusHandler(uow_factory)


# ============================================================================
# 4. Фабрики query-хендлеров (чтение) – используют read-репозиторий
# ============================================================================

async def get_list_customer_requests_handler(
    read_repo: CustomerRequestReadRepository = Depends(get_customer_request_read_repository),
) -> ListCustomerRequestsHandler:
    return ListCustomerRequestsHandler(read_repo)

async def get_customer_request_by_id_handler(
    read_repo: CustomerRequestReadRepository = Depends(get_customer_request_read_repository),
) -> GetCustomerRequestByIdHandler:
    return GetCustomerRequestByIdHandler(read_repo)


# ============================================================================
# 5. Медиатор (регистрация всех команд и запросов)
# ============================================================================

async def get_customer_requests_mediator(
    create_handler: CreateCustomerRequestHandler = Depends(get_create_customer_request_handler),
    change_status_handler: ChangeCustomerRequestStatusHandler = Depends(get_change_customer_request_status_handler),
    list_handler: ListCustomerRequestsHandler = Depends(get_list_customer_requests_handler),
    get_by_id_handler: GetCustomerRequestByIdHandler = Depends(get_customer_request_by_id_handler),
) -> Mediator:
    mediator = Mediator()

    # Регистрация команд (write)
    mediator.register(CreateCustomerRequestCommand, create_handler)
    mediator.register(ChangeCustomerRequestStatusCommand, change_status_handler)

    # Регистрация запросов (read)
    mediator.register(ListCustomerRequestsQuery, list_handler)
    mediator.register(GetCustomerRequestByIdQuery, get_by_id_handler)

    return mediator