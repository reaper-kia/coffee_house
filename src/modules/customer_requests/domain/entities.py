from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4
from decimal import Decimal

from .enums import CustomerRequestType, CustomerRequestStatus

@dataclass(frozen=True)
class CustomerRequestItem:
    menu_item_id: UUID
    title_snapshot: str
    price_amount_snapshot: Decimal
    price_currency_snapshot: str
    quantity: int
    comment: str | None = None

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if not self.title_snapshot.strip():
            raise ValueError("Title snapshot cannot be empty")

@dataclass
class CustomerRequest:
    id: UUID = field(default_factory=uuid4)
    request_type: CustomerRequestType
    customer_name: str
    contact: str
    desired_datetime: datetime
    person_count: int | None = None
    comment: str | None = None
    telegram_chat_id: str | None = None
    status: CustomerRequestStatus = CustomerRequestStatus.NEW
    _items: list[CustomerRequestItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def items(self):
        return tuple(self._items)

    @classmethod
    def create(
        cls,
        request_type: CustomerRequestType,
        customer_name: str,
        contact: str,
        desired_datetime: datetime,
        items: list[CustomerRequestItem],
        person_count: int | None = None,
        comment: str | None = None,
        telegram_chat_id: str | None = None,
    ) -> "CustomerRequest":
        if not customer_name.strip():
            raise ValueError("Customer name is required")
        if not contact.strip():
            raise ValueError("Contact is required")
        if person_count is not None and person_count <= 0:
            raise ValueError("Person count must be positive")
        if request_type == CustomerRequestType.PREORDER and not items:
            raise ValueError("PREORDER requires at least one item")
        return cls(
            request_type=request_type,
            customer_name=customer_name.strip(),
            contact=contact.strip(),
            desired_datetime=desired_datetime,
            person_count=person_count,
            comment=comment.strip() if comment else None,
            telegram_chat_id=telegram_chat_id.strip() if telegram_chat_id else None,
            _items=list(items),
        )

    def change_status(self, new_status: CustomerRequestStatus) -> None:
        allowed = {
            CustomerRequestStatus.NEW: {CustomerRequestStatus.CONFIRMED, CustomerRequestStatus.CANCELLED},
            CustomerRequestStatus.CONFIRMED: {CustomerRequestStatus.DONE, CustomerRequestStatus.CANCELLED},
            CustomerRequestStatus.CANCELLED: set(),
            CustomerRequestStatus.DONE: set(),
        }
        if new_status not in allowed[self.status]:
            raise ValueError(f"Cannot change from {self.status} to {new_status}")
        self.status = new_status
        self.updated_at = datetime.now(UTC)