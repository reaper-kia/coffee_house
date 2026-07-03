from dataclasses import dataclass
from uuid import UUID

@dataclass
class GetMenuItemQuery:
    menu_item_id: UUID