import pytest
from decimal import Decimal
from src.shared.domain.value_objects import Money
from src.modules.catalog.domain.value_objects import (
    CategoryTitle,
    ProductTitle,
    Description,
    Position,
)
from src.modules.catalog.domain.exceptions import (
    InvalidCategoryNameError,
    InvalidProductTitleError,
    InvalidCurrencyError,
    NegativeAmountError,
    InvalidPositionError,
)

def test_category_title_valid():
    title = CategoryTitle("Coffee")
    assert title.value == "Coffee"

def test_category_title_empty():
    with pytest.raises(InvalidCategoryNameError):
        CategoryTitle("")

def test_category_title_too_long():
    with pytest.raises(InvalidCategoryNameError):
        CategoryTitle("a" * 256)

def test_product_title_valid():
    title = ProductTitle("Cappuccino")
    assert title.value == "Cappuccino"

def test_product_title_empty():
    with pytest.raises(InvalidProductTitleError):
        ProductTitle("")

def test_product_title_too_long():
    with pytest.raises(InvalidProductTitleError):
        ProductTitle("a" * 256)

def test_description_valid():
    desc = Description("Valid description")
    assert desc.value == "Valid description"

def test_description_too_long():
    with pytest.raises(InvalidProductTitleError):  # но у нас InvalidProductDescriptionError?
        # Проверь, какое исключение используется в твоём VO
        Description("a" * 2001)

def test_money_valid():
    money = Money(amount=Decimal("10.50"), currency="EUR")
    assert money.currency == "EUR"
    assert money.amount == Decimal("10.50")

def test_money_invalid_currency():
    with pytest.raises(InvalidCurrencyError):
        Money(amount=Decimal("10"), currency="RUB")

def test_money_negative_amount():
    with pytest.raises(NegativeAmountError):
        Money(amount=Decimal("-1"), currency="USD")

def test_position_valid():
    pos = Position(5)
    assert pos.value == 5

def test_position_negative():
    with pytest.raises(InvalidPositionError):
        Position(-1)