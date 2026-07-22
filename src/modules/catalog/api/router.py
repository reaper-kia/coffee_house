# src/modules/catalog/api/router.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID
from typing import Optional, List

from src.shared.domain.exceptions import SharedDomainError
from src.modules.catalog.application.commands.change_menu_item_availability import ChangeMenuItemAvailabilityCommand
from src.shared.application.mediator import Mediator
from src.modules.auth.api.dependencies import require_admin

from src.modules.catalog.api.schemas import (
    CategoryResponse,
    MenuItemResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
    CreateMenuItemRequest,
    UpdateMenuItemRequest,
    ChangeAvailabilityRequest,
    menu_item_to_response,
    menu_item_read_model_to_response,
)
from src.modules.catalog.application.queries.get_categories import GetCategoriesQuery
from src.modules.catalog.application.queries.get_menu_items import GetMenuItemsQuery
from src.modules.catalog.application.queries.get_menu_item import GetMenuItemQuery
from src.modules.catalog.application.commands.create_menu_category import CreateMenuCategoryCommand
from src.modules.catalog.application.commands.update_menu_category import UpdateMenuCategoryCommand
from src.modules.catalog.application.commands.create_menu_item import CreateMenuItemCommand
from src.modules.catalog.application.commands.update_menu_item import UpdateMenuItemCommand
from src.modules.catalog.domain.exceptions import (
    CatalogDomainError,
    CategoryNotFoundError,
    MenuItemNotFoundError,
)

from .dependencies import get_catalog_mediator


router = APIRouter(prefix="/catalog", tags=["Catalog"])


# ============================================
# Публичные эндпоинты (без авторизации)
# ============================================

@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    mediator: Mediator = Depends(get_catalog_mediator),
):
    query = GetCategoriesQuery(active_only=True, limit=limit, offset=offset)
    categories = await mediator.send(query)
    return [CategoryResponse(**c.__dict__) for c in categories]


@router.get("/menu-items", response_model=List[MenuItemResponse])
async def get_menu_items(
    category_id: Optional[UUID] = None,
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    mediator: Mediator = Depends(get_catalog_mediator),
):
    query = GetMenuItemsQuery(
        category_id=category_id,
        available_only=True,
        search=search,
        limit=limit,
        offset=offset,
    )
    items = await mediator.send(query)
    return [MenuItemResponse(**i.__dict__) for i in items]


@router.get("/menu-items/{menu_item_id}", response_model=MenuItemResponse)
async def get_menu_item(
    menu_item_id: UUID,
    mediator: Mediator = Depends(get_catalog_mediator),
):
    query = GetMenuItemQuery(menu_item_id=menu_item_id)
    try:
        item = await mediator.send(query)
    except MenuItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return menu_item_read_model_to_response(item)


# ============================================
# Админские эндпоинты (требуют прав администратора)
# ============================================

admin_router = APIRouter(
    prefix="/admin/catalog",
    tags=["Admin Catalog"],
    dependencies=[Depends(require_admin)],
)


@admin_router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CreateCategoryRequest,
    mediator: Mediator = Depends(get_catalog_mediator),
):
    cmd = CreateMenuCategoryCommand(
        title=data.title,
        position=data.position,
        is_active=data.is_active,
    )
    try:
        category = await mediator.send(cmd)
    
    except CategoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    
    except (CatalogDomainError, SharedDomainError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    
    return CategoryResponse(
        id=category.id,
        title=category.title.value,
        is_active=category.is_active,
        position=category.position.value,
    )

@admin_router.patch("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    data: UpdateCategoryRequest,
    mediator: Mediator = Depends(get_catalog_mediator),
):
    cmd = UpdateMenuCategoryCommand(
        category_id=category_id,
        title=data.title,
        position=data.position,
        is_active=data.is_active,
    )
    try:
        category = await mediator.send(cmd)

    except CategoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except CatalogDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    
    return CategoryResponse(
        id=category.id,
        title=category.title.value,
        is_active=category.is_active,
        position=category.position.value,
    )


@admin_router.post("/menu-items", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def create_menu_item(
    data: CreateMenuItemRequest,
    mediator: Mediator = Depends(get_catalog_mediator),
):
    cmd = CreateMenuItemCommand(
        title=data.title,
        price_amount=data.price_amount,
        price_currency=data.price_currency,
        description=data.description,
        category_id=data.category_id,
        is_available=data.is_available,
        image_url=data.image_url,
        position=data.position,
    )
    try:
        item = await mediator.send(cmd)

    except CategoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except (CatalogDomainError, SharedDomainError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    return menu_item_to_response(item)

@admin_router.patch("/menu-items/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: UUID,
    data: UpdateMenuItemRequest,
    mediator: Mediator = Depends(get_catalog_mediator),
):
    cmd = UpdateMenuItemCommand(
        item_id=item_id,
        title=data.title,
        price_amount=data.price_amount,
        price_currency=data.price_currency,
        description=data.description,
        category_id=data.category_id,
        is_available=data.is_available,
        image_url=data.image_url,
        position=data.position,
    )
    try:
        item = await mediator.send(cmd)

    except (MenuItemNotFoundError, CategoryNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except (CatalogDomainError, SharedDomainError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    return menu_item_to_response(item)

@admin_router.patch("/menu-items/{item_id}/availability", response_model=MenuItemResponse)
async def change_availability(
    item_id: UUID,
    data: ChangeAvailabilityRequest,
    mediator: Mediator = Depends(get_catalog_mediator),
):
    cmd = ChangeMenuItemAvailabilityCommand(item_id=item_id, is_available=data.is_available)
    try:
        item = await mediator.send(cmd)
    except MenuItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return menu_item_to_response(item)

