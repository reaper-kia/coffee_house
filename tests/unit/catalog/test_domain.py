from decimal import Decimal
from uuid import UUID

import pytest

from src.modules.catalog.domain.entities import MenuCategory, MenuItem
from src.modules.catalog.domain.exceptions import (
    InvalidCategoryNameError,
    InvalidPositionError,
    InvalidProductDescriptionError,
    InvalidProductTitleError,
)
from src.modules.catalog.domain.value_objects import (
    CategoryTitle,
    Description,
    Position,
    ProductTitle,
)
from src.shared.domain.value_objects import Money


CATEGORY_ID = UUID("40000000-0000-0000-0000-000000000001")


@pytest.mark.unit
def test_catalog_value_objects_normalize_values() -> None:
    assert CategoryTitle(" Coffee ").value == "Coffee"
    assert ProductTitle(" Latte ").value == "Latte"
    assert Description(" Milk ").value == "Milk"
    assert Position(0).value == 0


@pytest.mark.unit
@pytest.mark.parametrize(
    ("factory", "value", "error"),
    [
        (CategoryTitle, " ", InvalidCategoryNameError),
        (ProductTitle, " ", InvalidProductTitleError),
        (Description, "x" * 2001, InvalidProductDescriptionError),
        (Position, -1, InvalidPositionError),
    ],
)
def test_catalog_value_objects_reject_invalid_values(factory, value, error) -> None:
    with pytest.raises(error):
        factory(value)


@pytest.mark.unit
def test_menu_category_changes_state() -> None:
    category = MenuCategory.create(
        title=CategoryTitle("Coffee"),
        position=Position(1),
        is_active=False,
    )

    category.change_title(CategoryTitle("Tea"))
    category.change_position(Position(2))
    category.activate()

    assert category.title.value == "Tea"
    assert category.position.value == 2
    assert category.is_active is True

    category.deactivate()
    assert category.is_active is False


@pytest.mark.unit
def test_menu_item_changes_state() -> None:
    item = MenuItem.create(
        title=ProductTitle("Latte"),
        price=Money(Decimal("4.50"), "EUR"),
        description=Description("Milk coffee"),
    )

    item.change_title(ProductTitle("Cappuccino"))
    item.change_description(Description("Foam"))
    item.change_price(Money(Decimal("5.00"), "EUR"))
    item.assign_category(CATEGORY_ID)
    item.change_image_url("https://example.test/item.png")
    item.mark_unavailable()

    assert item.title.value == "Cappuccino"
    assert item.description.value == "Foam"
    assert item.price.amount == Decimal("5.00")
    assert item.category_id == CATEGORY_ID
    assert item.image_url.endswith("item.png")
    assert item.is_available is False

    item.remove_category()
    item.mark_available()
    assert item.category_id is None
    assert item.is_available is True


@pytest.mark.unit
def test_menu_item_supports_position_change() -> None:
    item = MenuItem.create(
        title=ProductTitle("Latte"),
        price=Money(Decimal("4.50"), "EUR"),
        description=Description("Milk coffee"),
    )

    item.change_position(Position(7))

    assert item.position.value == 7
