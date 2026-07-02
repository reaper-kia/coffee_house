from dataclasses import dataclass

from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType


@dataclass(frozen=True)
class ListCustomerRequestsQuery:
    status: CustomerRequestStatus | None
    request_type: CustomerRequestType | None
    page: int
    page_size: int