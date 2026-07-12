import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from src.modules.catalog.application.handlers.create_menu_category import CreateMenuCategoryHandler
from src.modules.catalog.application.handlers.create_menu_item import CreateMenuItemHandler
from src.modules.catalog.application.commands.create_menu_category import CreateMenuCategoryCommand
from src.modules.catalog.application.commands.create_menu_item import CreateMenuItemCommand
from src.modules.catalog.domain.value_objects import CategoryTitle, ProductTitle, Description, Position
from src.shared.domain.value_objects import Money
from src.modules.catalog.domain.exceptions import CategoryNotFoundError

@pytest.mark.asyncio
async def test_create_category_success():
    repo = AsyncMock()
    uow_factory = MagicMock()
    uow_factory.return_value.__aenter__.return_value = MagicMock()
    handler = CreateMenuCategoryHandler(repo, uow_factory)
    cmd = CreateMenuCategoryCommand(
        title=CategoryTitle("Coffee"),
        position=Position(1),
        is_active=True,
    )
    category = await handler.handle(cmd)
    assert category.title.value == "Coffee"
    repo.save.assert_called_once()

@pytest.mark.asyncio
async def test_create_menu_item_success():
    item_repo = AsyncMock()
    category_repo = AsyncMock()
    category_repo.exists_by_id = AsyncMock(return_value=True)
    uow_factory = MagicMock()
    uow_factory.return_value.__aenter__.return_value = MagicMock()

    handler = CreateMenuItemHandler(item_repo, category_repo, uow_factory)
    cmd = CreateMenuItemCommand(
        title=ProductTitle("Latte"),
        price=Money(Decimal("5"), "EUR"),
        description=Description("Milk coffee"),
        category_id=uuid4(),
    )
    item = await handler.handle(cmd)
    assert item.title.value == "Latte"
    item_repo.save.assert_called_once()

@pytest.mark.asyncio
async def test_create_menu_item_category_not_found():
    category_repo = AsyncMock()
    category_repo.exists_by_id = AsyncMock(return_value=False)
    handler = CreateMenuItemHandler(AsyncMock(), category_repo, MagicMock())
    cmd = CreateMenuItemCommand(
        title=ProductTitle("Latte"),
        price=Money(Decimal("5"), "EUR"),
        description=Description("Milk"),
        category_id=uuid4(),
    )
    with pytest.raises(CategoryNotFoundError):
        await handler.handle(cmd)