from dataclasses import dataclass
from uuid import UUID

@dataclass
class ChangeMenuItemAvailabilityCommand:
    item_id: UUID
    is_available: bool