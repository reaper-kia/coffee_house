from dataclasses import dataclass
from uuid import UUID 

@dataclass(frozen=True)
class CreateOrderCommand:
    buyer_id: UUID
    items: list["CreateOrderItem"]

@dataclass(frozen=True)
class CreateOrderItem:
    menu_item_id: UUID
    quantity: int