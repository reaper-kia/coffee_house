import pytest
from decimal import Decimal
from src.modules.catalog.domain.entities import MenuCategory, MenuItem
from src.shared.domain.value_objects import Money
from src.modules.catalog.domain.value_objects import (
    CategoryTitle,
    ProductTitle,
    Description,
    Position,
)

def test_create_category():
    title = CategoryTitle("Coffee")
    category = MenuCategory.create(title=title, position=Position(1), is_active=True)
    assert category.title == title
    assert category.position.value == 1
    assert category.is_active is True

def test_category_activate():
    category = MenuCategory.create(CategoryTitle("Coffee"), Position(1), is_active=False)
    category.activate()
    assert category.is_active is True

def test_category_deactivate():
    category = MenuCategory.create(CategoryTitle("Coffee"), Position(1), is_active=True)
    category.deactivate()
    assert category.is_active is False

def test_create_menu_item():
    title = ProductTitle("Cappuccino")
    price = Money(Decimal("4.50"), "EUR")
    desc = Description("Delicious coffee")
    item = MenuItem.create(title=title, price=price, description=desc)
    assert item.title == title
    assert item.is_available is True
    assert item.position.value == 0

def test_menu_item_mark_available():
    item = MenuItem.create(
        ProductTitle("Latte"),
        Money(Decimal("5"), "EUR"),
        Description("Milk coffee")
    )
    item.mark_unavailable()
    assert item.is_available is False
    item.mark_available()
    assert item.is_available is True

def test_menu_item_change_price():
    item = MenuItem.create(
        ProductTitle("Latte"),
        Money(Decimal("5"), "EUR"),
        Description("Milk")
    )
    new_price = Money(Decimal("5.50"), "EUR")
    item.change_price(new_price)
    assert item.price == new_price