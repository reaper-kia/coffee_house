import hashlib
from decimal import Decimal
from typing import Any
from uuid import UUID

from src.modules.catalog.application.read_models import ProductReadModel
from src.shared.application.cache import JSONValue, JsonCache


CATALOG_PRODUCTS_LIST_PATTERN = "catalog:products:*"


def build_active_products_cache_key(
    *,
    category_ids: list[UUID] | None,
    limit: int,
    offset: int,
) -> str:
    category_part = _category_ids_cache_part(category_ids)
    
    
    return (
        "catalog:products:"
        f"active:categories:{category_part}:"
        f"limit:{limit}:offset:{offset}"
    )
    
def build_product_detail_cache_key(product_id: UUID) -> str:
    return f"catalog:product:{product_id}"

def product_to_cache_payload(product: ProductReadModel) -> dict[str, str | None]:
    return {
        "id": str(product.id),
        "owner_id": str(product.owner_id),
        "category_id": str(product.category_id) if product.category_id else None,
        "title": product.title,
        "description": product.description,
        "price_amount": str(product.price_amount),
        "price_currency": product.price_currency,
        "status": product.status,
    }

def products_to_cache_payload(products: list[ProductReadModel]) -> list[dict[str, str | None]]:
    return [product_to_cache_payload(product) for product in products]

def product_from_cache_payload(payload: dict[str, Any]) -> ProductReadModel:
    category_id = payload.get("category_id")
    
    return ProductReadModel(
        id=UUID(str(payload["id"])),
        owner_id=UUID(str(payload["owner_id"])),
        category_id=UUID(str(category_id)) if category_id else None,
        title=str(payload["title"]),
        description=str(payload["description"]),
        price_amount=Decimal(str(payload["price_amount"])),
        price_currency=str(payload["price_currency"]),
        status=str(payload["status"]),
    )

def products_from_cache_payload(payload: JSONValue) -> list[ProductReadModel]:
    if not isinstance(payload, list):
        raise ValueError("Cached products payload must be a list.")
    
    products: list[ProductReadModel] = []
    
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("Cached product item must be an object.")

        products.append(product_from_cache_payload(item))
    
    return products

async def invalidate_product_catalog_cache(
    *,
    cache: JsonCache,
    product_id: UUID,
) -> None:
    await cache.delete(build_product_detail_cache_key(product_id))
    await cache.delete_by_pattern(CATALOG_PRODUCTS_LIST_PATTERN)
    
async def invalidate_products_list_cache(
    *,
    cache: JsonCache,
) -> None:
    await cache.delete_by_pattern(CATALOG_PRODUCTS_LIST_PATTERN)
    
def _category_ids_cache_part(category_ids: list[UUID] | None) -> str:
    normalied_category_ids = sorted(str(category_id) for category_id in category_ids or [])
    
    if not normalied_category_ids:
        return "all"
    
    raw_value = ",".join(normalied_category_ids)
    
    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()[:16]