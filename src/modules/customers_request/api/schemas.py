from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class RequestCreateOrder(BaseModel):
    items: list["RequestCreateOrderItem"] = Field(min_length=1)

class RequestCreateOrderItem(BaseModel):
    menu_item_id: UUID
    quantity: int = Field(ge=1)

class ResponseOrder(BaseModel):
    id: UUID
    buyer_id: UUID
    total_price_amount: Decimal
    total_price_currency: str
    status: str
    items: list["ResponseOrderItem"]
    created_at: datetime

class ResponseOrderItem(BaseModel):
    menu_item_id: UUID
    title: str
    price_amount: Decimal
    price_currency: str
    quantity: int