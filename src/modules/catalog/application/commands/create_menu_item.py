from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

@dataclass
class CreateMenuItemCommand:
    title: str
    price_amount: Decimal
    price_currency: str
    description: str | None = None
    category_id: UUID | None = None
    is_available: bool = True
    image_url: str | None = None
    position: int = 0