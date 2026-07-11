# src/modules/catalog/api/schemas.py
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from src.modules.catalog.domain.entities import MenuCategory, MenuItem


class CategoryResponse(BaseModel):
    id: UUID
    title: str
    position: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class MenuItemResponse(BaseModel):
    id: UUID
    category_id: UUID | None = None
    category_title: str | None = None
    title: str
    description: str | None = None
    price_amount: Decimal = Field(..., decimal_places=2)
    price_currency: str
    image_url: str | None = None
    is_available: bool
    position: int

    model_config = ConfigDict(from_attributes=True)


# ============================================
# Запросы (для админских эндпоинтов)
# ============================================

class CreateCategoryRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    position: int = Field(0, ge=0)
    is_active: bool = True


class UpdateCategoryRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    position: int | None = Field(None, ge=0)
    is_active: bool | None = None


class CreateMenuItemRequest(BaseModel):
    category_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    price_amount: Decimal = Field(..., gt=0, decimal_places=2)
    price_currency: str = Field("EUR", pattern="^[A-Z]{3}$")
    image_url: str | None = Field(None, max_length=1000)
    is_available: bool = True
    position: int = Field(0, ge=0)


class UpdateMenuItemRequest(BaseModel):
    category_id: UUID | None = None
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    price_amount: Decimal | None = Field(None, gt=0, decimal_places=2)
    price_currency: str | None = Field(None, pattern="^[A-Z]{3}$")
    image_url: str | None = Field(None, max_length=1000)
    is_available: bool | None = None
    position: int | None = Field(None, ge=0)


class ChangeAvailabilityRequest(BaseModel):
    is_available: bool


def category_to_response(category: "MenuCategory") -> CategoryResponse:
    """Преобразует доменную сущность Category в Pydantic-схему."""
    return CategoryResponse(
        id=category.id,
        title=category.title.value,          # Извлекаем примитив из VO
        position=category.position.value,    # Извлекаем примитив из VO
        is_active=category.is_active,
    )


def menu_item_to_response(item: "MenuItem") -> MenuItemResponse:
    """Преобразует доменную сущность MenuItem в Pydantic-схему."""
    return MenuItemResponse(
        id=item.id,
        category_id=item.category_id,
        category_title=None,  # Заполняется из read-модели, если есть
        title=item.title.value,               # Из VO
        description=item.description.value,   # Из VO
        price_amount=item.price.amount,       # Из VO Money
        price_currency=item.price.currency,   # Из VO Money
        image_url=item.image_url,
        is_available=item.is_available,
        position=item.position.value,         # Из VO Position
    )