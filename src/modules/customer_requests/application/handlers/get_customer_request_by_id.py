from dataclasses import dataclass

from src.modules.customer_requests.application.queries.get_customer_request import (
    GetCustomerRequestByIdQuery,
)
from src.modules.customer_requests.application.read_models import CustomerRequestReadModel
from src.modules.customer_requests.application.ports.customer_request_read_repository import CustomerRequestReadRepository
from src.modules.customer_requests.domain.exceptions import CustomerRequestNotFound


@dataclass
class GetCustomerRequestByIdHandler:
    read_repo: CustomerRequestReadRepository

    async def handle(self, query: GetCustomerRequestByIdQuery) -> CustomerRequestReadModel:
        read_model = await self.read_repo.get_by_id(query.request_id)
        if read_model is None:
            raise CustomerRequestNotFound(
                f"Customer request {query.request_id} not found"
            )
        return read_model