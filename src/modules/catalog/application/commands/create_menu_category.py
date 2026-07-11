from dataclasses import dataclass

@dataclass
class CreateMenuCategoryCommand:
    title: str
    position: int = 0
    is_active: bool = True