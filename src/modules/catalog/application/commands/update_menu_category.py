from dataclasses import dataclass
from uuid import UUID
from src.modules.catalog.domain.value_objects import CategoryTitle, Position

@dataclass
class UpdateMenuCategoryCommand:
    category_id: UUID
    title: CategoryTitle | None = None
    position: Position | None = None
    is_active: bool | None = None