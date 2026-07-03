from dataclasses import dataclass
from decimal import Decimal

from src.modules.catalog.domain.exceptions import (
    InvalidCategoryNameError,
    InvalidProductDescriptionError,
    InvalidProductTitleError,
    InvalidCurrencyError,
    NegativeAmountError,
    InvalidPositionError,
)

ALLOWED_CURRENCIES = {"USD", "EUR"}


@dataclass(frozen=True)
class ProductTitle:
    value: str

    def __post_init__(self):
        normalized = self.value.strip()
        if not normalized:
            raise InvalidProductTitleError("Product title cannot be empty")
        if len(normalized) > 255:
            raise InvalidProductTitleError("Product title is too long")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class CategoryTitle:
    value: str

    def __post_init__(self):
        normalized = self.value.strip()
        if not normalized:
            raise InvalidCategoryNameError("Category name cannot be empty")
        if len(normalized) > 255:
            raise InvalidCategoryNameError("Category name is too long")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class Description:
    value: str

    def __post_init__(self):
        normalized = self.value.strip()
        if len(normalized) > 2000:
            raise InvalidProductDescriptionError("Description is too long")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        normalized_currency = self.currency.strip().upper()
        if normalized_currency not in ALLOWED_CURRENCIES:
            raise InvalidCurrencyError(f"Invalid currency: {self.currency}")
        if self.amount < 0:
            raise NegativeAmountError(f"Amount cannot be negative: {self.amount}")
        object.__setattr__(self, "currency", normalized_currency)


@dataclass(frozen=True)
class Position:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise InvalidPositionError(f"Position cannot be negative: {self.value}")