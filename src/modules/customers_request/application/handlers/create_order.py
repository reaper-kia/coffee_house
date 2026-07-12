from dataclasses import dataclass


from src.modules.customers_request.application.commands.create_order import CreateOrderCommand
from src.modules.customers_request.application.ports.product_snapshot_provider import ProductSnapshotProvider
from src.modules.customers_request.domain.entities import Order, OrderItem
from src.modules.customers_request.domain.exceptions import ProductForOrderNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory
from src.shared.domain.value_objects import Money

@dataclass
class CreateOrderCommandHandler:
    uow_factory: UnitOfWorkFactory
    product_snapshot_provider: ProductSnapshotProvider
    
    async def handle(self, cmd: CreateOrderCommand) -> Order:
        order_items: list[OrderItem] = []
        
        for item in cmd.items:
            product_snapshot = await self.product_snapshot_provider.get_active_product_snapshot(item.menu_item_id)

            if product_snapshot is None:
                raise ProductForOrderNotFoundError("Active product not found")
            
            order_items.append(
                OrderItem(
                    menu_item_id=product_snapshot.menu_item_id,
                    menu_item_title_snapshot=product_snapshot.title,
                    price_snapshot=Money(
                        amount=product_snapshot.price_snapshot_amount,
                        currency=product_snapshot.price_snapshot_currency,
                        ),
                    quantity=item.quantity,
                )
            )
        
        order = Order.create(
            buyer_id=cmd.buyer_id,
            items=order_items,
        )
            
        async with self.uow_factory() as uow:
            await uow.orders.add(order)
            await uow.commit()
        
        return order