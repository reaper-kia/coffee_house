from dataclasses import dataclass

from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType

@dataclass(frozen=True)
class ListCustomerRequestsQuery:
    status: CustomerRequestStatus | None = None
    request_type: CustomerRequestType | None = None
    page: int = 1
    page_size: int = 20