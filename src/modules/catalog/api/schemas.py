# src/modules/catalog/api/schemas.py
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


# ============================================
# Ответы (для публичных и админских эндпоинтов)
# ============================================

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