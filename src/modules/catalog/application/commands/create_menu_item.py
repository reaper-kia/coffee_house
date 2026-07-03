from dataclasses import dataclass
from uuid import UUID
from src.modules.catalog.domain.value_objects import ProductTitle, Money, Description, Position

@dataclass
class CreateMenuItemCommand:
    title: ProductTitle
    price: Money
    description: Description
    category_id: UUID | None = None
    is_available: bool = True
    image_url: str | None = None
    position: Position = Position(0)