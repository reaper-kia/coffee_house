from dataclasses import dataclass
from typing import Optional

from src.modules.catalog.domain.exceptions import (
    InvalidCategoryNameError,
    InvalidProductDescriptionError,
    InvalidProductTitleError,
    InvalidPositionError,
)


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
    value: Optional[str] = None

    def __post_init__(self):
        if self.value is None:
            return
        normalized = self.value.strip()
        if len(normalized) > 2000:
            raise InvalidProductDescriptionError("Description is too long")
        object.__setattr__(self, "value", normalized)

@dataclass(frozen=True)
class Position:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise InvalidPositionError(f"Position cannot be negative: {self.value}")