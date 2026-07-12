from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.customers_request.application.commands.create_order import CreateOrderCommand
from src.modules.customers_request.application.handlers.create_order import CreateOrderCommandHandler
from src.modules.customers_request.application.handlers.get_by_id import GetOrderByIdQueryHandler
from src.modules.customers_request.application.ports.order_repository import OrderReadRepository
from src.modules.customers_request.application.ports.product_snapshot_provider import ProductSnapshotProvider
from src.modules.customers_request.application.queries.get_by_id import GetOrderByIdQuery
from src.modules.customers_request.infra.product_snapshot_provider import SQLAlchemyProductSnapshotProvider
from src.modules.customers_request.infra.repositories import SQLAlchemyOrderReadRepository
from src.shared.api.dependencies import get_unit_of_work_factory
from src.shared.application.mediator import Mediator
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.shared.infra.database.session import get_async_session


def get_product_snapshot_provider(
    session: AsyncSession = Depends(get_async_session),
) -> ProductSnapshotProvider:
    return SQLAlchemyProductSnapshotProvider(
        session=session,
    )


def get_order_read_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OrderReadRepository:
    return SQLAlchemyOrderReadRepository(
        session=session,
    )


def get_create_order_handler(
    uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory),
    product_snapshot_provider: ProductSnapshotProvider = Depends(
        get_product_snapshot_provider
    ),
) -> CreateOrderCommandHandler:
    return CreateOrderCommandHandler(
        uow_factory=uow_factory,
        product_snapshot_provider=product_snapshot_provider,
    )


def get_order_by_id_handler(
    order_read_repository: OrderReadRepository = Depends(get_order_read_repository),
) -> GetOrderByIdQueryHandler:
    return GetOrderByIdQueryHandler(
        order_read_repository=order_read_repository,
    )


def get_order_mediator(
    create_order_handler: CreateOrderCommandHandler = Depends(
        get_create_order_handler
    ),
    order_by_id_handler: GetOrderByIdQueryHandler = Depends(
        get_order_by_id_handler
    ),
) -> Mediator:
    mediator = Mediator()

    mediator.register(CreateOrderCommand, create_order_handler)
    mediator.register(GetOrderByIdQuery, order_by_id_handler)

    return mediator