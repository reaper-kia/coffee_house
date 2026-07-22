from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.modules.catalog.application.commands.change_menu_item_availability import (
    ChangeMenuItemAvailabilityCommand,
)
from src.modules.catalog.application.commands.create_menu_category import (
    CreateMenuCategoryCommand,
)
from src.modules.catalog.application.commands.create_menu_item import (
    CreateMenuItemCommand,
)
from src.modules.catalog.application.commands.update_menu_item import (
    UpdateMenuItemCommand,
)
from src.modules.catalog.application.handlers.change_menu_item_availability import (
    ChangeMenuItemAvailabilityHandler,
)
from src.modules.catalog.application.handlers.create_menu_category import (
    CreateMenuCategoryHandler,
)
from src.modules.catalog.application.handlers.create_menu_item import (
    CreateMenuItemHandler,
)
from src.modules.catalog.application.handlers.update_menu_item import (
    UpdateMenuItemHandler,
)
from src.modules.catalog.domain.entities import MenuItem
from src.modules.catalog.domain.exceptions import (
    CategoryNotFoundError,
    MenuItemNotFoundError,
)
from src.modules.catalog.domain.value_objects import Description, ProductTitle
from src.shared.domain.value_objects import Money
from tests.fakes import FakeUoW, FakeUoWFactory


CATEGORY_ID = UUID("41000000-0000-0000-0000-000000000001")
ITEM_ID = UUID("41000000-0000-0000-0000-000000000002")


def make_item() -> MenuItem:
    item = MenuItem.create(
        title=ProductTitle("Latte"),
        price=Money(Decimal("4.50"), "EUR"),
        description=Description("Milk coffee"),
        category_id=CATEGORY_ID,
    )
    item.id = ITEM_ID
    return item


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_category_handler_commits() -> None:
    categories = SimpleNamespace(save=AsyncMock())
    uow = FakeUoW(menu_categories=categories)
    handler = CreateMenuCategoryHandler(FakeUoWFactory(uow))

    category = await handler.handle(
        CreateMenuCategoryCommand("Coffee", position=1, is_active=True)
    )

    assert category.title.value == "Coffee"
    categories.save.assert_awaited_once_with(category)
    uow.commit.assert_awaited_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_menu_item_uses_single_transaction() -> None:
    categories = SimpleNamespace(exists_by_id=AsyncMock(return_value=True))
    items = SimpleNamespace(save=AsyncMock())
    uow = FakeUoW(menu_categories=categories, menu_items=items)
    factory = FakeUoWFactory(uow)
    handler = CreateMenuItemHandler(factory)

    item = await handler.handle(
        CreateMenuItemCommand(
            title="Latte",
            price_amount=Decimal("4.50"),
            price_currency="EUR",
            description="Milk coffee",
            category_id=CATEGORY_ID,
        )
    )

    assert factory.calls == 1
    categories.exists_by_id.assert_awaited_once_with(CATEGORY_ID)
    items.save.assert_awaited_once_with(item)
    uow.commit.assert_awaited_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_menu_item_allows_missing_description() -> None:
    items = SimpleNamespace(save=AsyncMock())
    uow = FakeUoW(
        menu_categories=SimpleNamespace(
            exists_by_id=AsyncMock(return_value=True)
        ),
        menu_items=items,
    )
    handler = CreateMenuItemHandler(FakeUoWFactory(uow))

    item = await handler.handle(
        CreateMenuItemCommand(
            title="Espresso",
            price_amount=Decimal("3.00"),
            price_currency="EUR",
            description=None,
            category_id=None,
        )
    )

    assert item.description.value == ""


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_menu_item_rejects_unknown_category() -> None:
    categories = SimpleNamespace(exists_by_id=AsyncMock(return_value=False))
    items = SimpleNamespace(save=AsyncMock())
    uow = FakeUoW(menu_categories=categories, menu_items=items)
    handler = CreateMenuItemHandler(FakeUoWFactory(uow))

    with pytest.raises(CategoryNotFoundError):
        await handler.handle(
            CreateMenuItemCommand(
                title="Latte",
                price_amount=Decimal("4.50"),
                price_currency="EUR",
                description="Milk",
                category_id=CATEGORY_ID,
            )
        )

    items.save.assert_not_awaited()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_menu_item_updates_position() -> None:
    item = make_item()
    items = SimpleNamespace(
        get_by_id=AsyncMock(return_value=item),
        save=AsyncMock(),
    )
    categories = SimpleNamespace(exists_by_id=AsyncMock(return_value=True))
    uow = FakeUoW(menu_items=items, menu_categories=categories)
    handler = UpdateMenuItemHandler(FakeUoWFactory(uow))

    updated = await handler.handle(
        UpdateMenuItemCommand(item_id=ITEM_ID, position=9)
    )

    assert updated.position.value == 9
    items.save.assert_awaited_once_with(item)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_menu_item_rejects_missing_item() -> None:
    items = SimpleNamespace(get_by_id=AsyncMock(return_value=None))
    uow = FakeUoW(menu_items=items)
    handler = UpdateMenuItemHandler(FakeUoWFactory(uow))

    with pytest.raises(MenuItemNotFoundError):
        await handler.handle(UpdateMenuItemCommand(item_id=ITEM_ID))


@pytest.mark.unit
@pytest.mark.asyncio
async def test_change_availability_handler() -> None:
    item = make_item()
    items = SimpleNamespace(
        get_by_id=AsyncMock(return_value=item),
        save=AsyncMock(),
    )
    uow = FakeUoW(menu_items=items)
    handler = ChangeMenuItemAvailabilityHandler(FakeUoWFactory(uow))

    result = await handler.handle(
        ChangeMenuItemAvailabilityCommand(ITEM_ID, False)
    )

    assert result.is_available is False
    items.save.assert_awaited_once_with(item)
    uow.commit.assert_awaited_once()
