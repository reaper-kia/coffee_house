from typing import Protocol
from uuid import UUID

from src.modules.customers_request.application.read_models import OrderReadModel
from src.modules.customers_request.domain.entities import Order


class OrderRepository(Protocol):
    async def add(self, order: Order):
        ...
    
    async def get_by_id(self, id: UUID) -> Order | None:
        ...
    
    async def save(self, order: Order):
        ...

class OrderReadRepository(Protocol):
    async def get_by_id(self, id: UUID) -> OrderReadModel | None:
        ...