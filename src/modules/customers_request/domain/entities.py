from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4


from src.modules.customers_request.domain.exceptions import DifferentCurrencyInOrderError, EmptyOrderError, InvalidOrderStatusTransitionError, InvalidQuantityError
from src.modules.customers_request.domain.value_objects import OrderStatus
from src.shared.domain.value_objects import Money

@dataclass
class Order:
    buyer_id: UUID
    total_price: Money
    id: UUID = field(default_factory=uuid4)
    status: OrderStatus = OrderStatus.CREATED
    _items: list["OrderItem"] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    @property
    def items(self) -> tuple["OrderItem", ...]:
        return tuple(self._items)
    
    @classmethod
    def create(cls, buyer_id: UUID, items: list["OrderItem"]) -> "Order":
        if len(items) <= 0:
            raise EmptyOrderError("Cannot create order without items")
        
        currency = items[0].price_snapshot.currency

        for item in items:
            if item.price_snapshot.currency != currency:
                raise DifferentCurrencyInOrderError("Different currency error")

        total_amount = sum(
            (item.price_snapshot.amount * item.quantity for item in items),
            Decimal("0"),
        )
        
        return cls(
            buyer_id=buyer_id,
            _items=list(items),
            total_price=Money(
                amount=total_amount, 
                currency=currency
                ), 
        )
    
    def __post_init__(self) -> None:
        if not self.items:
            raise EmptyOrderError("Cannot create order without items")

        currency = self.items[0].price_snapshot.currency

        for item in self.items:
            if item.price_snapshot.currency != currency:
                raise DifferentCurrencyInOrderError(
                    "All order items must have the same currency"
                )

        expected_total_amount = sum(
            (item.price_snapshot.amount * item.quantity for item in self.items),
            Decimal("0"),
        )

        expected_total_price = Money(
            amount=expected_total_amount,
            currency=currency,
        )

        if self.total_price != expected_total_price:
            raise ValueError("Order total price does not match order items")
    
    def mark_paid(self) -> None:
        if self.status != OrderStatus.CREATED:
            raise InvalidOrderStatusTransitionError("Only created order can be paid")

        self.status = OrderStatus.PAID
        
@dataclass 
class OrderItem:
    menu_item_id: UUID
    menu_item_title_snapshot: str
    price_snapshot: Money
    quantity: int
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise InvalidQuantityError("Quantity must be greater than zero")
        if not self.menu_item_title_snapshot.strip():
            raise ValueError("Product title snapshot cannot be empty")
        