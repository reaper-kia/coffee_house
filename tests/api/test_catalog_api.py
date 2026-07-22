
import pytest

from src.modules.auth.api.dependencies import require_admin
from src.modules.catalog.api.dependencies import get_catalog_mediator
from src.modules.catalog.domain.exceptions import (
    CategoryNotFoundError,
    MenuItemNotFoundError,
)
from tests.factories import (
    CATEGORY_ID,
    ITEM_ID,
    category_entity,
    category_read_model,
    menu_item_entity,
    menu_item_read_model,
)
from tests.fakes import StubMediator


@pytest.mark.api
@pytest.mark.asyncio
async def test_public_categories(app, client) -> None:
    mediator = StubMediator(result=[category_read_model()])
    app.dependency_overrides[get_catalog_mediator] = lambda: mediator

    response = await client.get("/api/v1/catalog/categories")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(CATEGORY_ID),
            "title": "Coffee",
            "position": 1,
            "is_active": True,
        }
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_public_menu_items(app, client) -> None:
    app.dependency_overrides[get_catalog_mediator] = lambda: StubMediator(
        result=[menu_item_read_model()]
    )

    response = await client.get("/api/v1/catalog/menu-items")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "Latte"
    assert response.json()[0]["category_title"] == "Coffee"
    assert response.json()[0]["price_amount"] == "4.50"


@pytest.mark.api
@pytest.mark.asyncio
async def test_public_menu_item_by_id_uses_read_model(app, client) -> None:
    app.dependency_overrides[get_catalog_mediator] = lambda: StubMediator(
        result=menu_item_read_model()
    )

    response = await client.get(f"/api/v1/catalog/menu-items/{ITEM_ID}")

    assert response.status_code == 200
    assert response.json()["id"] == str(ITEM_ID)
    assert response.json()["category_title"] == "Coffee"


@pytest.mark.api
@pytest.mark.asyncio
async def test_public_menu_item_not_found(app, client) -> None:
    app.dependency_overrides[get_catalog_mediator] = lambda: StubMediator(
        error=MenuItemNotFoundError("menu_item_not_found")
    )

    response = await client.get(f"/api/v1/catalog/menu-items/{ITEM_ID}")

    assert response.status_code == 404
    assert response.json()["detail"] == "menu_item_not_found"


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_catalog_requires_authentication(app, client) -> None:
    response = await client.post(
        "/api/v1/admin/catalog/categories",
        json={"title": "Coffee", "position": 1, "is_active": True},
    )

    assert response.status_code == 401


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_creates_category(app, client, admin_user) -> None:
    mediator = StubMediator(result=category_entity())
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_catalog_mediator] = lambda: mediator

    response = await client.post(
        "/api/v1/admin/catalog/categories",
        json={"title": "Coffee", "position": 1, "is_active": True},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Coffee"
    assert mediator.messages[0].title == "Coffee"


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_create_item_maps_category_not_found(app, client, admin_user) -> None:
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_catalog_mediator] = lambda: StubMediator(
        error=CategoryNotFoundError("Category not found")
    )

    response = await client.post(
        "/api/v1/admin/catalog/menu-items",
        json={
            "category_id": str(CATEGORY_ID),
            "title": "Latte",
            "description": "Milk",
            "price_amount": "4.50",
            "price_currency": "EUR",
        },
    )

    assert response.status_code == 404


@pytest.mark.api
@pytest.mark.asyncio
@pytest.mark.parametrize("currency", ["GBP", "RUB", "eur"])
async def test_admin_create_item_rejects_unsupported_currency(
    app,
    client,
    admin_user,
    currency: str,
) -> None:
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_catalog_mediator] = lambda: StubMediator(
        result=menu_item_entity()
    )

    response = await client.post(
        "/api/v1/admin/catalog/menu-items",
        json={
            "title": "Latte",
            "description": "Milk",
            "price_amount": "4.50",
            "price_currency": currency,
        },
    )

    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_update_item_rejects_partial_price(app, client, admin_user) -> None:
    app.dependency_overrides[require_admin] = lambda: admin_user
    app.dependency_overrides[get_catalog_mediator] = lambda: StubMediator(
        result=menu_item_entity()
    )

    response = await client.patch(
        f"/api/v1/admin/catalog/menu-items/{ITEM_ID}",
        json={"price_amount": "5.00"},
    )

    assert response.status_code == 422
