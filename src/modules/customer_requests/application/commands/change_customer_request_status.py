from dataclasses import dataclass
from uuid import UUID
from src.modules.customer_requests.domain.enums import CustomerRequestStatus

@dataclass(frozen=True)
class ChangeCustomerRequestStatusCommand:
    request_id: UUID
    new_status: CustomerRequestStatus
    changed_by_admin_id: UUID