from unittest.mock import AsyncMock, MagicMock

import pytest

from src.shared.infra.database.unit_of_work import SQLAlchemyUnitOfWork


@pytest.mark.unit
@pytest.mark.asyncio
async def test_sqlalchemy_uow_initializes_all_repositories() -> None:
    session = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    factory = MagicMock(return_value=session)
    uow = SQLAlchemyUnitOfWork(factory)

    entered = await uow.__aenter__()

    assert entered is uow
    assert uow.users is not None
    assert uow.outbox is not None
    assert uow.notification_deliveries is not None
    assert uow.processed_kafka_messages is not None
    assert uow.menu_categories is not None
    assert uow.menu_items is not None
    assert uow.customer_requests is not None
    assert uow.menu_item_snapshots is not None

    await uow.__aexit__(None, None, None)
    session.close.assert_awaited_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_sqlalchemy_uow_rolls_back_on_exception() -> None:
    session = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    uow = SQLAlchemyUnitOfWork(MagicMock(return_value=session))
    await uow.__aenter__()

    await uow.__aexit__(RuntimeError, RuntimeError("boom"), None)

    session.rollback.assert_awaited_once()
    session.close.assert_awaited_once()
