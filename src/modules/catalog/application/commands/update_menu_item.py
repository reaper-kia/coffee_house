from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

@dataclass
class UpdateMenuItemCommand:
    item_id: UUID
    title: str | None = None
    description: str | None = None
    price_amount: Decimal | None = None
    price_currency: str | None = None
    category_id: UUID | None = None
    is_available: bool | None = None
    image_url: str | None = None
    position: int | None = None