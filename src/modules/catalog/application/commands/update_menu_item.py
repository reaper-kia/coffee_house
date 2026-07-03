from dataclasses import dataclass
from uuid import UUID
from src.modules.catalog.domain.value_objects import ProductTitle, Money, Description, Position

@dataclass
class UpdateMenuItemCommand:
    item_id: UUID
    title: ProductTitle | None = None
    price: Money | None = None
    description: Description | None = None
    category_id: UUID | None = None
    is_available: bool | None = None
    image_url: str | None = None
    position: Position | None = None