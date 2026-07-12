from typing import Protocol

from uuid import UUID

from src.modules.customers_request.application.read_models import ProductSnapshot


class ProductSnapshotProvider(Protocol):
    async def get_active_product_snapshot(self, menu_item_id: UUID) -> ProductSnapshot | None:
        ...