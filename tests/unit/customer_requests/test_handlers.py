from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.modules.customer_requests.application.commands.change_customer_request_status import (
    ChangeCustomerRequestStatusCommand,
)
from src.modules.customer_requests.application.commands.create_customer_request import (
    CreateCustomerRequestCommand,
    CreateCustomerRequestItem,
)
from src.modules.customer_requests.application.handlers.change_customer_request_status import (
    ChangeCustomerRequestStatusHandler,
)
from src.modules.customer_requests.application.handlers.create_customer_request import (
    CreateCustomerRequestHandler,
)
from src.modules.customer_requests.application.handlers.get_customer_request_by_id import (
    GetCustomerRequestByIdHandler,
)
from src.modules.customer_requests.application.handlers.list_customer_requests import (
    ListCustomerRequestsHandler,
)
from src.modules.customer_requests.application.ports.menu_item_snapshot_repository import (
    ProductSnapshot,
)
from src.modules.customer_requests.application.queries.get_customer_request import (
    GetCustomerRequestByIdQuery,
)
from src.modules.customer_requests.application.queries.list_customer_requests import (
    ListCustomerRequestsQuery,
)
from src.modules.customer_requests.application.read_models import (
    CustomerRequestPageReadModel,
)
from src.modules.customer_requests.domain.entities import CustomerRequest
from src.modules.customer_requests.domain.enums import (
    CustomerRequestStatus,
    CustomerRequestType,
)
from src.modules.customer_requests.domain.exceptions import (
    CustomerRequestNotFound,
    MenuItemUnavailable,
)
from tests.fakes import FakeUoW, FakeUoWFactory


REQUEST_ID = UUID("51000000-0000-0000-0000-000000000001")
ITEM_ID = UUID("51000000-0000-0000-0000-000000000002")
ADMIN_ID = UUID("51000000-0000-0000-0000-000000000003")
DESIRED_AT = datetime(2026, 8, 1, 18, tzinfo=UTC)


def make_request() -> CustomerRequest:
    request = CustomerRequest.create(
        request_type=CustomerRequestType.TABLE_BOOKING,
        customer_name="Alice",
        contact="+49123",
        desired_datetime=DESIRED_AT,
        person_count=2,
        items=[],
    )
    request.id = REQUEST_ID
    return request


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_preorder_uses_snapshots_and_commits_once() -> None:
    snapshot = ProductSnapshot(
        menu_item_id=ITEM_ID,
        title="Latte",
        price_amount=Decimal("4.50"),
        price_currency="EUR",
    )
    snapshot_repo = SimpleNamespace(
        get_available_by_ids=AsyncMock(return_value={ITEM_ID: snapshot})
    )
    request_repo = SimpleNamespace(add=AsyncMock())
    uow = FakeUoW(
        menu_item_snapshots=snapshot_repo,
        customer_requests=request_repo,
    )
    factory = FakeUoWFactory(uow)
    handler = CreateCustomerRequestHandler(factory)

    result = await handler.handle(
        CreateCustomerRequestCommand(
            request_type=CustomerRequestType.PREORDER,
            customer_name="Alice",
            contact="+49123",
            desired_datetime=DESIRED_AT,
            person_count=2,
            comment=None,
            telegram_chat_id="12345",
            items=[CreateCustomerRequestItem(ITEM_ID, 2)],
        )
    )

    assert factory.calls == 1
    assert result.items[0].title_snapshot == "Latte"
    assert result.items[0].price_amount_snapshot == Decimal("4.50")
    request_repo.add.assert_awaited_once_with(result)
    uow.commit.assert_awaited_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_preorder_rejects_missing_snapshot() -> None:
    request_repo = SimpleNamespace(add=AsyncMock())
    uow = FakeUoW(
        menu_item_snapshots=SimpleNamespace(
            get_available_by_ids=AsyncMock(return_value={})
        ),
        customer_requests=request_repo,
    )
    handler = CreateCustomerRequestHandler(FakeUoWFactory(uow))

    with pytest.raises(MenuItemUnavailable, match=str(ITEM_ID)):
        await handler.handle(
            CreateCustomerRequestCommand(
                request_type=CustomerRequestType.PREORDER,
                customer_name="Alice",
                contact="+49123",
                desired_datetime=DESIRED_AT,
                person_count=None,
                comment=None,
                telegram_chat_id=None,
                items=[CreateCustomerRequestItem(ITEM_ID, 1)],
            )
        )

    request_repo.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_change_status_handler_updates_entity() -> None:
    request = make_request()
    repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=request),
        save=AsyncMock(),
    )
    uow = FakeUoW(customer_requests=repo)
    handler = ChangeCustomerRequestStatusHandler(FakeUoWFactory(uow))

    result = await handler.handle(
        ChangeCustomerRequestStatusCommand(
            request_id=REQUEST_ID,
            new_status=CustomerRequestStatus.CONFIRMED,
            changed_by_admin_id=ADMIN_ID,
        )
    )

    assert result.status is CustomerRequestStatus.CONFIRMED
    repo.save.assert_awaited_once_with(request)
    uow.commit.assert_awaited_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_change_status_handler_rejects_missing_request() -> None:
    uow = FakeUoW(
        customer_requests=SimpleNamespace(
            get_by_id=AsyncMock(return_value=None),
            save=AsyncMock(),
        )
    )
    handler = ChangeCustomerRequestStatusHandler(FakeUoWFactory(uow))

    with pytest.raises(CustomerRequestNotFound):
        await handler.handle(
            ChangeCustomerRequestStatusCommand(
                REQUEST_ID,
                CustomerRequestStatus.CONFIRMED,
                ADMIN_ID,
            )
        )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_list_handler_calculates_offset() -> None:
    page = CustomerRequestPageReadModel(items=[], total=0)
    repo = SimpleNamespace(list=AsyncMock(return_value=page))
    handler = ListCustomerRequestsHandler(repo)

    result = await handler.handle(
        ListCustomerRequestsQuery(page=3, page_size=20)
    )

    assert result == page
    repo.list.assert_awaited_once_with(
        status=None,
        request_type=None,
        limit=20,
        offset=40,
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_handler_rejects_missing_request() -> None:
    repo = SimpleNamespace(get_by_id=AsyncMock(return_value=None))
    handler = GetCustomerRequestByIdHandler(repo)

    with pytest.raises(CustomerRequestNotFound):
        await handler.handle(GetCustomerRequestByIdQuery(REQUEST_ID))
