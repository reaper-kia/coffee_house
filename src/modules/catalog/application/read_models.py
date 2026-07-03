from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

@dataclass
class CategoryReadModel:
    id: UUID
    title: str
    position: int
    is_active: bool

@dataclass
class MenuItemReadModel:
    id: UUID
    category_id: UUID | None
    category_title: str | None
    title: str
    description: str | None
    price_amount: Decimal
    price_currency: str
    image_url: str | None
    is_available: bool
    position: int