from pydantic import BaseModel

from src.modules.customer_requests.api.schemas import CustomerRequestResponse


class AdminCustomerRequestsPageResponse(BaseModel):
    items: list[CustomerRequestResponse]
    total: int
    page: int
    page_size: int
    total_pages: int