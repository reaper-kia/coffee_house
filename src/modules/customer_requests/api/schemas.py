from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class RequestItemResponse(BaseModel):
    menu_item_id: UUID
    title: str
    quantity: int
    price_amount: Decimal
    price_currency: str
    comment: str | None = None

class CustomerRequestResponse(BaseModel):
    id: UUID
    request_type: str
    customer_name: str
    contact: str
    desired_datetime: datetime
    person_count: int | None = None
    comment: str | None = None
    status: str
    items: list[RequestItemResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

