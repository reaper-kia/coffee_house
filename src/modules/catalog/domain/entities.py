from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.modules.catalog.domain.value_objects import CategoryTitle, Description, Position, ProductTitle
from src.shared.domain.value_objects import Money

@dataclass
class MenuItem:
    title: ProductTitle
    price: Money
    description: Description
    category_id: UUID | None = None
    is_available: bool = True
    image_url: str | None = None
    position: Position = field(default_factory=lambda: Position(0))
    id: UUID = field(default_factory=uuid4)
    
    @classmethod
    def create(cls,
        title: ProductTitle,
        price: Money,
        description: Description,
        is_available: bool = True,
        category_id: UUID | None = None,
        image_url: str | None = None,
        position: Position = Position(0),
        ) -> "MenuItem":
        return cls(
            title=title,
            description=description,
            price=price,
            is_available = is_available,
            category_id=category_id,
            image_url=image_url,
            position=position,
        )
        
    def change_title(self, title: ProductTitle):
        self.title = title
    
    def change_description(self, description: Description):
        self.description = description
    
    def assign_category(self, category_id: UUID):
        self.category_id = category_id
    
    def remove_category(self) -> None:
        self.category_id = None
    
    def change_price(self, new_price: Money) -> None:
        self.price = new_price
    
    def change_image_url(self, new_image_url: str | None) -> None:
        self.image_url = new_image_url

    def mark_available(self) -> None:
        self.is_available = True

    def mark_unavailable(self) -> None:
        self.is_available = False
    def change_position(self, new_position: Position) -> None:
        self.position = new_position
        


@dataclass
class MenuCategory:
    title: CategoryTitle
    position: Position = field(default_factory=lambda: Position(0))
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def create(cls,
        title: CategoryTitle,
        position: Position = Position(0),
        is_active: bool = True,
    ) -> "MenuCategory":
        return cls(
            title=title,
            position=position,
            is_active=is_active,
        )

    def change_title(self, new_title: CategoryTitle) -> None:
        self.title = new_title

    def change_position(self, new_position: Position) -> None:
        self.position = new_position

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False