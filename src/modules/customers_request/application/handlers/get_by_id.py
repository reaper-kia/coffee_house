from dataclasses import dataclass

from src.modules.customers_request.application.ports.order_repository import OrderReadRepository
from src.modules.customers_request.application.queries.get_by_id import GetOrderByIdQuery
from src.modules.customers_request.application.read_models import OrderReadModel
from src.modules.customers_request.domain.exceptions import OrderAccessDeniedError, OrderNotFoundError

@dataclass
class GetOrderByIdQueryHandler:
    order_read_repository: OrderReadRepository
    
    async def handle(self, query: GetOrderByIdQuery) -> OrderReadModel:
        read_model = await self.order_read_repository.get_by_id(query.order_id)
        
        if read_model is None:
            raise OrderNotFoundError("Order not found")
        
        if read_model.buyer_id != query.buyer_id:
            raise OrderAccessDeniedError("You cannot access this order")
        
        return read_model