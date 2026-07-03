from dataclasses import dataclass
from uuid import UUID

@dataclass
class DeleteMenuItemCommand:
    item_id: UUID