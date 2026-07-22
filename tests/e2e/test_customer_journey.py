from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.modules.auth.api.dependencies import require_admin
from src.modules.catalog.api.dependencies import get_catalog_mediator
from src.modules.catalog.application.commands.change_menu_item_availability import (
    ChangeMenuItemAvailabilityCommand,
)
from src.modules.catalog.application.commands.create_menu_category import (
    CreateMenuCategoryCommand,
)
from src.modules.catalog.application.commands.create_menu_item import (
    CreateMenuItemCommand,
)
from src.modules.catalog.application.queries.get_categories import GetCategoriesQuery
from src.modules.catalog.application.queries.get_menu_items import GetMenuItemsQuery
from src.modules.catalog.application.read_models import CategoryReadModel, MenuItemReadModel
from src.modules.catalog.domain.entities import MenuCategory, MenuItem
from src.modules.catalog.domain.value_objects import (
    CategoryTitle,
    Description,
    Position,
    ProductTitle,
)
from src.modules.customer_requests.api.dependencies import (
    get_customer_requests_mediator,
)
from src.modules.customer_requests.application.commands.change_customer_request_status import (
    ChangeCustomerRequestStatusCommand,
)
from src.modules.customer_requests.application.commands.create_customer_request import (
    CreateCustomerRequestCommand,
)
from src.modules.customer_requests.application.queries.list_customer_requests import (
    ListCustomerRequestsQuery,
)
from src.modules.customer_requests.application.read_models import (
    CustomerRequestItemReadModel,
    CustomerRequestPageReadModel,
    CustomerRequestReadModel,
)
from src.modules.customer_requests.domain.entities import (
    CustomerRequest,
    CustomerRequestItem,
)
from src.modules.customer_requests.domain.enums import CustomerRequestStatus
from src.shared.domain.value_objects import Money


class CatalogStateMediator:
    def __init__(self) -> None:
        self.categories: dict[UUID, MenuCategory] = {}
        self.items: dict[UUID, MenuItem] = {}

    async def send(self, message):
        if isinstance(message, CreateMenuCategoryCommand):
            category = MenuCategory.create(
                CategoryTitle(message.title),
                Position(message.position),
                message.is_active,
            )
            self.categories[category.id] = category
            return category

        if isinstance(message, CreateMenuItemCommand):
            item = MenuItem.create(
                ProductTitle(message.title),
                Money(message.price_amount, message.price_currency),
                Description(message.description or ""),
                message.is_available,
                message.category_id,
                message.image_url,
                Position(message.position),
            )
            self.items[item.id] = item
            return item

        if isinstance(message, ChangeMenuItemAvailabilityCommand):
            item = self.items[message.item_id]
            if message.is_available:
                item.mark_available()
            else:
                item.mark_unavailable()
            return item

        if isinstance(message, GetCategoriesQuery):
            return [
                CategoryReadModel(
                    id=category.id,
                    title=category.title.value,
                    position=category.position.value,
                    is_active=category.is_active,
                )
                for category in self.categories.values()
                if not message.active_only or category.is_active
            ]

        if isinstance(message, GetMenuItemsQuery):
            result = []
            for item in self.items.values():
                if message.available_only and not item.is_available:
                    continue
                category = self.categories.get(item.category_id)
                result.append(
                    MenuItemReadModel(
                        id=item.id,
                        category_id=item.category_id,
                        category_title=(category.title.value if category else None),
                        title=item.title.value,
                        description=item.description.value,
                        price_amount=item.price.amount,
                        price_currency=item.price.currency,
                        image_url=item.image_url,
                        is_available=item.is_available,
                        position=item.position.value,
                    )
                )
            return result

        raise AssertionError(f"Unsupported catalog message: {type(message).__name__}")


class RequestStateMediator:
    def __init__(self, catalog: CatalogStateMediator) -> None:
        self.catalog = catalog
        self.requests: dict[UUID, CustomerRequest] = {}

    async def send(self, message):
        if isinstance(message, CreateCustomerRequestCommand):
            items = []
            for requested in message.items:
                menu_item = self.catalog.items[requested.menu_item_id]
                items.append(
                    CustomerRequestItem(
                        menu_item_id=menu_item.id,
                        title_snapshot=menu_item.title.value,
                        price_amount_snapshot=menu_item.price.amount,
                        price_currency_snapshot=menu_item.price.currency,
                        quantity=requested.quantity,
                        comment=requested.comment,
                    )
                )
            request = CustomerRequest.create(
                request_type=message.request_type,
                customer_name=message.customer_name,
                contact=message.contact,
                desired_datetime=message.desired_datetime,
                person_count=message.person_count,
                comment=message.comment,
                telegram_chat_id=message.telegram_chat_id,
                items=items,
            )
            self.requests[request.id] = request
            return request

        if isinstance(message, ListCustomerRequestsQuery):
            models = [self._to_read_model(item) for item in self.requests.values()]
            return CustomerRequestPageReadModel(items=models, total=len(models))

        if isinstance(message, ChangeCustomerRequestStatusCommand):
            request = self.requests[message.request_id]
            request.change_status(message.new_status)
            return request

        raise AssertionError(f"Unsupported request message: {type(message).__name__}")

    @staticmethod
    def _to_read_model(request: CustomerRequest) -> CustomerRequestReadModel:
        return CustomerRequestReadModel(
            id=request.id,
            request_type=request.request_type,
            customer_name=request.customer_name,
            contact=request.contact,
            telegram_chat_id=request.telegram_chat_id,
            desired_datetime=request.desired_datetime,
            person_count=request.person_count,
            comment=request.comment,
            status=request.status,
            items=[
                CustomerRequestItemReadModel(
                    menu_item_id=item.menu_item_id,
                    title=item.title_snapshot,
                    quantity=item.quantity,
                    price_amount=item.price_amount_snapshot,
                    price_currency=item.price_currency_snapshot,
                    comment=item.comment,
                )
                for item in request.items
            ],
            created_at=request.created_at,
            updated_at=request.updated_at,
        )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_catalog_preorder_and_admin_confirmation(app, client, admin_user) -> None:
    catalog = CatalogStateMediator()
    requests = RequestStateMediator(catalog)
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_catalog_mediator] = lambda: catalog
    app.dependency_overrides[get_customer_requests_mediator] = lambda: requests

    category_response = await client.post(
        "/api/v1/admin/catalog/categories",
        json={"title": "Coffee", "position": 1, "is_active": True},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    item_response = await client.post(
        "/api/v1/admin/catalog/menu-items",
        json={
            "category_id": category_id,
            "title": "Latte",
            "description": "Milk coffee",
            "price_amount": "4.50",
            "price_currency": "EUR",
            "position": 1,
        },
    )
    assert item_response.status_code == 201
    item_id = item_response.json()["id"]

    public_items = await client.get("/api/v1/catalog/menu-items")
    assert public_items.status_code == 200
    assert [item["title"] for item in public_items.json()] == ["Latte"]

    request_response = await client.post(
        "/api/v1/customer-requests",
        json={
            "request_type": "PREORDER",
            "customer_name": "Alice",
            "contact": "+49123",
            "telegram_chat_id": "12345",
            "desired_datetime": datetime(2026, 8, 1, 18, tzinfo=UTC).isoformat(),
            "person_count": 2,
            "items": [{"menu_item_id": item_id, "quantity": 2}],
        },
    )
    assert request_response.status_code == 201
    request_id = request_response.json()["id"]
    assert request_response.json()["items"][0]["price_amount"] == "4.50"

    admin_list = await client.get("/admin/customer-requests")
    assert admin_list.status_code == 200
    assert admin_list.json()["total"] == 1

    confirmed = await client.patch(
        f"/admin/customer-requests/{request_id}/status?status=CONFIRMED"
    )
    assert confirmed.status_code == 200
    assert confirmed.json()["status"] == CustomerRequestStatus.CONFIRMED.value
