import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_categories(client):
    response = await client.get("/api/v1/catalog/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_menu_items(client):
    response = await client.get("/api/v1/catalog/menu-items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_menu_item_not_found(client):
    response = await client.get("/api/v1/catalog/menu-items/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu_item_not_found"