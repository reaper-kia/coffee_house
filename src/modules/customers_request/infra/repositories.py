from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from src.modules.customers_request.application.ports.order_repository import OrderReadRepository, OrderRepository
from src.modules.customers_request.application.read_models import OrderItemReadModel, OrderReadModel
from src.modules.customers_request.domain.entities import Order, OrderItem
from src.modules.customers_request.domain.exceptions import OrderNotFoundError
from src.modules.customers_request.domain.value_objects import OrderStatus
from src.modules.customers_request.infra.models import OrderItemModel, OrderModel
from src.shared.domain.value_objects import Money


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, order: Order) -> None:
        model = OrderModel(
            id=order.id,
            buyer_id=order.buyer_id,
            status=order.status.value,
            total_price_amount=order.total_price.amount,
            total_price_currency=order.total_price.currency,
            created_at=order.created_at,
            items=[
                OrderItemModel(
                    menu_item_id=item.menu_item_id,
                    menu_item_title_snapshot=item.menu_item_title_snapshot,
                    price_amount_snapshot=item.price_snapshot.amount,
                    price_currency_snapshot=item.price_snapshot.currency,
                    quantity=item.quantity,
                )
                for item in order.items
            ],
        )
        self.session.add(model)
    
    async def get_by_id(self, id: UUID) -> Order | None:
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return self._to_domain(model)
    
    async def save(self, order: Order):
        stmt=select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id == order.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            raise OrderNotFoundError("Order not found")
        
        model.status = order.status.value
        model.total_price_amount = order.total_price.amount
        model.total_price_currency = order.total_price.currency
        model.created_at = order.created_at
        model.items = [
            OrderItemModel(
                menu_item_id=item.menu_item_id,
                menu_item_title_snapshot=item.menu_item_title_snapshot,
                price_amount_snapshot=item.price_snapshot.amount,
                price_currency_snapshot=item.price_snapshot.currency,
                quantity=item.quantity,
            )
            for item in order.items
        ]
        
    
    @staticmethod
    def _to_domain(model: OrderModel) -> Order:
        return Order(
            id=model.id,
            buyer_id=model.buyer_id,
            total_price=Money(
                amount=model.total_price_amount,
                currency=model.total_price_currency,
            ),
            status=OrderStatus(model.status),
            created_at=model.created_at,
            _items=list(
                OrderItem(
                    menu_item_id=m.menu_item_id,
                    menu_item_title_snapshot=m.menu_item_title_snapshot,
                    price_snapshot=Money(
                        amount=m.price_amount_snapshot,
                        currency=m.price_currency_snapshot,
                    ),
                    quantity=m.quantity,
                )
                for m in model.items
            ),
        )

class SQLAlchemyOrderReadRepository(OrderReadRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def get_by_id(self, id: UUID) -> OrderReadModel | None:
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return OrderReadModel(
            id=model.id,
            buyer_id=model.buyer_id,
            total_price_amount=model.total_price_amount,
            total_price_currency=model.total_price_currency,
            status=model.status,
            items=[
                OrderItemReadModel(
                    menu_item_id=item.menu_item_id,
                    menu_item_title_snapshot=item.menu_item_title_snapshot,
                    price_amount_snapshot=item.price_amount_snapshot,
                    price_currency_snapshot=item.price_currency_snapshot,
                    quantity=item.quantity,
                )
                for item in model.items
            ],
            created_at=model.created_at,
        )