from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType


@dataclass(frozen=True)
class CustomerRequestItemReadModel:
    """Read-модель для элемента заявки."""
    menu_item_id: UUID
    title: str
    quantity: int
    price_amount: Decimal
    price_currency: str
    comment: str | None = None


@dataclass(frozen=True)
class CustomerRequestReadModel:
    """Read-модель для заявки (оптимизирована для отображения)."""
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
    """Read-модель для страницы заявок (с пагинацией)."""
    items: list[CustomerRequestReadModel]
    total: int