from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class GetMenuItemsQuery:
    category_id: Optional[UUID] = None
    available_only: bool = True
    search: Optional[str] = None
    limit: int = 50
    offset: int = 0