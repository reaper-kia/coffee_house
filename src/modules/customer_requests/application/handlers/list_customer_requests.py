from dataclasses import dataclass

from src.modules.customer_requests.application.queries.list_customer_requests import (
    ListCustomerRequestsQuery,
)
from src.modules.customer_requests.application.read_models import CustomerRequestPageReadModel
from src.modules.customer_requests.application.ports.customer_request_read_repository import CustomerRequestReadRepository


@dataclass
class ListCustomerRequestsHandler:
    read_repo: CustomerRequestReadRepository

    async def handle(self, query: ListCustomerRequestsQuery) -> CustomerRequestPageReadModel:
        offset = (query.page - 1) * query.page_size
        limit = query.page_size
        return await self.read_repo.list(
            status=query.status,
            request_type=query.request_type,
            limit=limit,
            offset=offset,
        )