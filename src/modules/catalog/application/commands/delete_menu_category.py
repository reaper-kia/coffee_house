from dataclasses import dataclass
from uuid import UUID

@dataclass
class DeleteMenuCategoryCommand:
    category_id: UUID