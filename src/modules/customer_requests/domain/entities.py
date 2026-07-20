from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from src.modules.customer_requests.domain.exceptions import CustomerRequestEmptyError, CustomerRequestInvalidPersonCountError, CustomerRequestInvalidTypeError, CustomerRequestItemInvalidCommentError, CustomerRequestItemInvalidPriceError, CustomerRequestItemInvalidQuantityError, CustomerRequestItemInvalidTitleError, CustomerRequestStatusInvalidTransition
from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType

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
            raise CustomerRequestItemInvalidQuantityError("Quantity must be greater than zero")
        
        if self.quantity > 100:
            raise CustomerRequestItemInvalidQuantityError("Quantity cannot exceed 100")

        if not self.title_snapshot.strip():
            raise CustomerRequestItemInvalidTitleError("Product title snapshot cannot be empty")
        if len(self.title_snapshot) > 255:
            raise CustomerRequestItemInvalidTitleError("Title snapshot too long (max 255)")
        
        if self.price_amount_snapshot <= 0:
            raise CustomerRequestItemInvalidPriceError("Price amount must be positive")
        
        if self.comment is not None and len(self.comment) > 500:
            raise CustomerRequestItemInvalidCommentError("Comment too long (max 500)")



@dataclass
class CustomerRequest:
    request_type: CustomerRequestType
    customer_name: str
    contact: str
    desired_datetime: datetime
    id: UUID = field(default_factory=uuid4)
    person_count: int | None = None
    comment: str | None = None
    telegram_chat_id: str | None = None
    status: CustomerRequestStatus = CustomerRequestStatus.NEW
    _items: list[CustomerRequestItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    @property
    def items(self) -> tuple["CustomerRequestItem", ...]:
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
        # 1. Валидация бизнес-правил
        if not customer_name.strip():
            raise CustomerRequestEmptyError("Customer name is required")
        if not contact.strip():
            raise CustomerRequestEmptyError("Contact is required")
        if person_count is not None and person_count <= 0:
            raise CustomerRequestInvalidPersonCountError("Person count must be positive")
        if request_type == CustomerRequestType.PREORDER and not items:
            raise CustomerRequestInvalidTypeError("PREORDER requires at least one item")

        # 2. Создание объекта
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
        # Разрешённые переходы
        allowed = {
            CustomerRequestStatus.NEW: {
                CustomerRequestStatus.CONFIRMED,
                CustomerRequestStatus.CANCELLED,
            },
            CustomerRequestStatus.CONFIRMED: {
                CustomerRequestStatus.DONE,
                CustomerRequestStatus.CANCELLED,
            },
            CustomerRequestStatus.CANCELLED: set(),
            CustomerRequestStatus.DONE: set(),
        }
        if new_status not in allowed[self.status]:
            raise CustomerRequestStatusInvalidTransition(
                f"Cannot change status from {self.status} to {new_status}"
            )
        self.status = new_status
        self.updated_at = datetime.now(UTC)