# src/modules/customer_requests/api/router.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID
from typing import Optional, List

from src.shared.application.mediator import Mediator
from src.modules.auth.api.dependencies import get_current_user_id, require_admin

from src.modules.customer_requests.api.schemas import (
    CreateCustomerRequestRequest,
    CustomerRequestPageResponse,
    CustomerRequestResponse,
    customer_request_read_model_to_response,
    customer_request_to_response,          # маппер для ответа
)
from src.modules.customer_requests.application.commands.create_customer_request import (
    CreateCustomerRequestCommand,
    CreateCustomerRequestItem,
)
from src.modules.customer_requests.application.commands.change_customer_request_status import (
    ChangeCustomerRequestStatusCommand,
)
from src.modules.customer_requests.application.queries.list_customer_requests import (
    ListCustomerRequestsQuery,
)
from src.modules.customer_requests.application.queries.get_customer_request import (
    GetCustomerRequestByIdQuery,
)
from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType
from src.modules.customer_requests.domain.exceptions import (
    CustomerRequestNotFound,
    MenuItemUnavailable,
    InvalidCustomerRequest,
    CustomerRequestStatusInvalidTransition,
)

from .dependencies import get_customer_requests_mediator


# ============================================
# Публичные эндпоинты (без авторизации)
# ============================================

router = APIRouter(prefix="/customer-requests", tags=["Customer Requests"])


@router.post(
    "/",
    response_model=CustomerRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_request(
    data: CreateCustomerRequestRequest,
    mediator: Mediator = Depends(get_customer_requests_mediator),
) -> CustomerRequestResponse:
    """
    Создание новой заявки (публичный эндпоинт).
    Не требует авторизации.
    """
    # Формируем команду
    command = CreateCustomerRequestCommand(
        request_type=data.request_type,
        customer_name=data.customer_name,
        contact=data.contact,
        desired_datetime=data.desired_datetime,
        person_count=data.person_count,
        comment=data.comment,
        telegram_chat_id=data.telegram_chat_id,
        items=[
            CreateCustomerRequestItem(
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                comment=item.comment,
            )
            for item in data.items
        ],
    )

    try:
        request_entity = await mediator.send(command)
    except (MenuItemUnavailable, InvalidCustomerRequest) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    # Другие ошибки (например, проблемы с БД) обрабатываются глобально

    return customer_request_to_response(request_entity)


# ============================================
# Админские эндпоинты (требуют прав администратора)
# ============================================

admin_router = APIRouter(
    prefix="/admin/customer-requests",
    tags=["Admin Customer Requests"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("/", response_model=CustomerRequestPageResponse)
async def list_customer_requests(
    status: Optional[CustomerRequestStatus] = None,
    request_type: Optional[CustomerRequestType] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    mediator: Mediator = Depends(get_customer_requests_mediator),
) -> CustomerRequestPageResponse:
    """
    Получить список заявок с фильтрами и пагинацией (админский).
    """
    query = ListCustomerRequestsQuery(
        status=status,
        request_type=request_type,
        page=page,
        page_size=page_size,
    )
    page_result = await mediator.send(query)

    # Преобразуем read-модели в response-схемы
    items = [customer_request_read_model_to_response(item) for item in page_result.items]
    return CustomerRequestPageResponse(
        items=items,
        total=page_result.total,
        page=page,
        page_size=page_size,
    )


@admin_router.get("/{request_id}", response_model=CustomerRequestResponse)
async def get_customer_request(
    request_id: UUID,
    mediator: Mediator = Depends(get_customer_requests_mediator),
) -> CustomerRequestResponse:
    """
    Получить заявку по ID (админский).
    """
    query = GetCustomerRequestByIdQuery(request_id=request_id)
    try:
        read_model = await mediator.send(query)
    except CustomerRequestNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    # Преобразуем read-модель в response (она уже содержит все поля)
    return customer_request_read_model_to_response(read_model)


@admin_router.patch("/{request_id}/status", response_model=CustomerRequestResponse)
async def change_customer_request_status(
    request_id: UUID,
    new_status: CustomerRequestStatus,  # или использовать схему с полем status
    mediator: Mediator = Depends(get_customer_requests_mediator),
    admin_id: UUID = Depends(get_current_user_id),  # предположим, есть такая зависимость
) -> CustomerRequestResponse:
    """
    Изменить статус заявки (админский).
    """
    command = ChangeCustomerRequestStatusCommand(
        request_id=request_id,
        new_status=new_status,
        changed_by_admin_id=admin_id,
    )
    try:
        request_entity = await mediator.send(command)
    except CustomerRequestNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCustomerRequestStatusTransition as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return customer_request_to_response(request_entity)