import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_category_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "title": "Tea",
        "position": 2,
        "is_active": True,
    }
    response = await client.post("/api/v1/admin/catalog/categories", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Tea"
    assert data["is_active"] is True
    assert "id" in data

@pytest.mark.asyncio
async def test_create_menu_item_admin(client, admin_token):
    # Сначала создадим категорию
    headers = {"Authorization": f"Bearer {admin_token}"}
    cat_resp = await client.post(
        "/api/v1/admin/catalog/categories",
        json={"title": "Coffee", "position": 1, "is_active": True},
        headers=headers,
    )
    assert cat_resp.status_code == 201
    category_id = cat_resp.json()["id"]

    item_payload = {
        "category_id": category_id,
        "title": "Cappuccino",
        "description": "Espresso with milk",
        "price_amount": "4.50",
        "price_currency": "EUR",
        "is_available": True,
        "position": 1,
    }
    item_resp = await client.post(
        "/api/v1/admin/catalog/menu-items",
        json=item_payload,
        headers=headers,
    )
    assert item_resp.status_code == 201
    data = item_resp.json()
    assert data["title"] == "Cappuccino"
    assert data["category_id"] == category_id

@pytest.mark.asyncio
async def test_create_menu_item_invalid_category(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "category_id": "00000000-0000-0000-0000-000000000000",
        "title": "Invalid",
        "description": "Invalid category",
        "price_amount": "10.00",
        "price_currency": "EUR",
        "is_available": True,
        "position": 1,
    }
    response = await client.post("/api/v1/admin/catalog/menu-items", json=payload, headers=headers)
    assert response.status_code == 404
    assert "Category" in response.json()["detail"]