from dataclasses import dataclass

@dataclass
class GetCategoriesQuery:
    active_only: bool = True
    limit: int = 100
    offset: int = 0