from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.catalog.infra.models import MenuItemModel
from src.modules.customers_request.application.ports.product_snapshot_provider import ProductSnapshotProvider
from src.modules.customers_request.application.read_models import ProductSnapshot


class SQLAlchemyProductSnapshotProvider(ProductSnapshotProvider):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_active_product_snapshot(self, menu_item_id: UUID) -> ProductSnapshot | None:
        stmt=select(
            MenuItemModel.id,
            MenuItemModel.title,
            MenuItemModel.price_amount,
            MenuItemModel.price_currency,
        ).where(
            MenuItemModel.id == menu_item_id,
            MenuItemModel.is_available == True,
        )
        result = await self.session.execute(stmt)
        row = result.one_or_none()
        
        if row is None:
            return None
        
        return ProductSnapshot(
            menu_item_id=row.id,
            title=row.title,
            price_snapshot_amount=row.price_amount,
            price_snapshot_currency=row.price_currency,
        )