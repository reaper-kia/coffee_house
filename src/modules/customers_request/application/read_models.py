from dataclasses import dataclass

from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class ProductSnapshot:
    menu_item_id: UUID
    title: str
    price_snapshot_amount: Decimal 
    price_snapshot_currency: str 

@dataclass(frozen=True)
class OrderReadModel:
    id: UUID
    buyer_id: UUID
    total_price_amount: Decimal
    total_price_currency: str
    status: str
    items: list["OrderItemReadModel"]
    created_at: datetime

@dataclass(frozen=True)
class OrderItemReadModel:
    menu_item_id: UUID
    menu_item_title_snapshot: str
    price_amount_snapshot: Decimal 
    price_currency_snapshot: str 
    quantity: int