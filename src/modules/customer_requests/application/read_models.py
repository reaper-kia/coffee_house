from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType

@dataclass(frozen = True)
class CustomerRequestItemReadModel:
    menu_item_id: UUID
    title: str
    quantity: int
    price_amount: Decimal
    price_currency: str
    comment: str | None = None

@dataclass(frozen = True)
class CustomerRequestReadModel:
    id: UUID
    request_type: CustomerRequestType
    customer_name: str
    contact: str
    telegram_chat_id: str | None
    desired_datetime: datetime
    person_count: int | None
    comment: str | None
    status: CustomerRequestStatus
    items: list[CustomerRequestItemReadModel]
    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True)
class CustomerRequestPageReadModel:
    items: list[CustomerRequestReadModel]
    total: int