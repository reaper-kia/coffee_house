from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.modules.customer_requests.domain.enums import CustomerRequestType

@dataclass(frozen=True)
class CreateCustomerRequestItem:
    menu_item_id: UUID
    quantity: int
    comment: str | None = None

@dataclass(frozen=True)
class CreateCustomerRequestCommand:
    request_type: CustomerRequestType
    customer_name: str
    contact: str
    desired_datetime: datetime
    person_count: int | None
    comment: str | None
    telegram_chat_id: str | None
    items: list[CreateCustomerRequestItem]