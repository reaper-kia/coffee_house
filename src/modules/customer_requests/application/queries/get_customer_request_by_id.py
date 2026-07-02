from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetCustomerRequestByIdQuery:
    request_id: UUID