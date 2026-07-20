import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from src.modules.customer_requests.domain.enums import (
    CustomerRequestStatus,
    CustomerRequestType,
)

class CustomerRequestItemCreate(BaseModel):
    menu_item_id: UUID
    quantity: int = Field(ge=1, le=100)
    comment: str | None = Field(default=None, max_length=500)

class CreateCustomerRequestRequest(BaseModel):
    request_type: CustomerRequestType
    customer_name: str = Field(min_length=1, max_length=255)
    contact: str = Field(min_length=1, max_length=255)
    telegram_chat_id: str | None = Field(default=None, max_length=64)
    desired_datetime: datetime
    person_count: int | None = Field(default=None, ge=1, le=500)
    comment: str | None = Field(default=None, max_length=2000)
    items: list[CustomerRequestItemCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_request_type(self):
        if self.request_type == CustomerRequestType.PREORDER and not self.items:
            raise ValueError("PREORDER must contain at least one item")
        return self

class CustomerRequestItemResponse(BaseModel):
    menu_item_id: UUID
    title: str
    quantity: int
    price_amount: Decimal
    price_currency: str
    comment: str | None = None

class CustomerRequestResponse(BaseModel):
    id: UUID
    request_type: CustomerRequestType
    customer_name: str
    contact: str
    telegram_chat_id: str | None = None
    desired_datetime: datetime
    person_count: int | None = None
    comment: str | None = None
    status: CustomerRequestStatus
    items: list[CustomerRequestItemResponse]
    created_at: datetime
    updated_at: datetime