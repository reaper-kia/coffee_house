from dataclasses import dataclass
from src.modules.catalog.domain.value_objects import CategoryTitle, Position

@dataclass
class CreateMenuCategoryCommand:
    title: CategoryTitle
    position: Position = Position(0)
    is_active: bool = True