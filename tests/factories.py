from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from src.modules.catalog.application.read_models import (
    CategoryReadModel,
    MenuItemReadModel,
)
from src.modules.catalog.domain.entities import MenuCategory, MenuItem
from src.modules.catalog.domain.value_objects import (
    CategoryTitle,
    Description,
    Position,
    ProductTitle,
)
from src.modules.customer_requests.application.read_models import (
    CustomerRequestItemReadModel,
    CustomerRequestReadModel,
)
from src.modules.customer_requests.domain.entities import CustomerRequest
from src.modules.customer_requests.domain.enums import (
    CustomerRequestStatus,
    CustomerRequestType,
)
from src.modules.users.application.read_models import UserReadModel
from src.shared.domain.value_objects import Money


CATEGORY_ID = UUID("90000000-0000-0000-0000-000000000001")
ITEM_ID = UUID("90000000-0000-0000-0000-000000000002")
REQUEST_ID = UUID("90000000-0000-0000-0000-000000000003")
USER_ID = UUID("90000000-0000-0000-0000-000000000004")
DESIRED_AT = datetime(2026, 8, 1, 18, tzinfo=UTC)


def category_entity() -> MenuCategory:
    category = MenuCategory.create(CategoryTitle("Coffee"), Position(1), True)
    category.id = CATEGORY_ID
    return category


def category_read_model() -> CategoryReadModel:
    return CategoryReadModel(CATEGORY_ID, "Coffee", 1, True)


def menu_item_entity() -> MenuItem:
    item = MenuItem.create(
        ProductTitle("Latte"),
        Money(Decimal("4.50"), "EUR"),
        Description("Milk coffee"),
        category_id=CATEGORY_ID,
        position=Position(1),
    )
    item.id = ITEM_ID
    return item


def menu_item_read_model() -> MenuItemReadModel:
    return MenuItemReadModel(
        id=ITEM_ID,
        category_id=CATEGORY_ID,
        category_title="Coffee",
        title="Latte",
        description="Milk coffee",
        price_amount=Decimal("4.50"),
        price_currency="EUR",
        image_url=None,
        is_available=True,
        position=1,
    )


def customer_request_entity() -> CustomerRequest:
    request = CustomerRequest.create(
        request_type=CustomerRequestType.TABLE_BOOKING,
        customer_name="Alice",
        contact="+49123",
        desired_datetime=DESIRED_AT,
        person_count=2,
        comment="Window",
        telegram_chat_id="12345",
        items=[],
    )
    request.id = REQUEST_ID
    return request


def customer_request_read_model() -> CustomerRequestReadModel:
    now = datetime(2026, 7, 22, 12, tzinfo=UTC)
    return CustomerRequestReadModel(
        id=REQUEST_ID,
        request_type=CustomerRequestType.PREORDER,
        customer_name="Alice",
        contact="+49123",
        telegram_chat_id="12345",
        desired_datetime=DESIRED_AT,
        person_count=2,
        comment="Window",
        status=CustomerRequestStatus.NEW,
        items=[
            CustomerRequestItemReadModel(
                menu_item_id=ITEM_ID,
                title="Latte",
                quantity=2,
                price_amount=Decimal("4.50"),
                price_currency="EUR",
                comment=None,
            )
        ],
        created_at=now,
        updated_at=now,
    )


def user_read_model(*, is_admin: bool = False) -> UserReadModel:
    return UserReadModel(
        id=USER_ID,
        name="Alice",
        email="alice@example.com",
        is_admin=is_admin,
    )
