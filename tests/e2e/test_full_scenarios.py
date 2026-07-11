# tests/e2e/test_full_scenarios.py
from uuid import uuid4

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_admin_flow(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Создать категорию
    cat_resp = await client.post(
        "/api/v1/admin/catalog/categories",
        json={"title": "Coffee", "position": 1, "is_active": True},
        headers=headers,
    )
    assert cat_resp.status_code == 201
    category = cat_resp.json()
    category_id = category["id"]

    # 2. Создать позицию меню
    item_resp = await client.post(
        "/api/v1/admin/catalog/menu-items",
        json={
            "category_id": category_id,
            "title": "Cappuccino",
            "description": "Espresso with milk foam",
            "price_amount": "4.50",
            "price_currency": "EUR",
            "is_available": True,
            "position": 1,
        },
        headers=headers,
    )
    assert item_resp.status_code == 201
    item = item_resp.json()
    item_id = item["id"]

    # 3. Изменить доступность
    avail_resp = await client.patch(
        f"/api/v1/admin/catalog/menu-items/{item_id}/availability",
        json={"is_available": False},
        headers=headers,
    )
    assert avail_resp.status_code == 200
    assert avail_resp.json()["is_available"] is False

    # 4. Проверить, что публичный эндпоинт с available_only=true не возвращает этот товар
    public_resp = await client.get("/api/v1/catalog/menu-items?available_only=true")
    assert public_resp.status_code == 200
    items = public_resp.json()
    assert not any(i["id"] == item_id for i in items)

@pytest.mark.asyncio
async def test_negative_create_menu_item(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "category_id": str(uuid4()),  # несуществующая категория
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