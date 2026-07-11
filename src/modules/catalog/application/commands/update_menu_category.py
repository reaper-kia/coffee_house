from dataclasses import dataclass
from uuid import UUID

@dataclass
class UpdateMenuCategoryCommand:
    category_id: UUID
    title: str | None = None
    position: int | None = None
    is_active: bool | None = None