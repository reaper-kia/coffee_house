# src/modules/customer_requests/api/router.py

from fastapi import APIRouter, Depends, HTTPException, status

from src.shared.application.mediator import Mediator

from src.modules.customer_requests.api.schemas import (
    CreateCustomerRequestRequest,
    CustomerRequestResponse,
    customer_request_to_response,          # маппер для ответа
)
from src.modules.customer_requests.application.commands.create_customer_request import (
    CreateCustomerRequestCommand,
    CreateCustomerRequestItem,
)

from src.modules.customer_requests.domain.exceptions import (
    CustomerRequestException,
)

from .dependencies import get_customer_requests_mediator


# ============================================
# Публичные эндпоинты (без авторизации)
# ============================================

router = APIRouter(prefix="/customer-requests", tags=["Customer Requests"])


@router.post(
    "",
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
    except CustomerRequestException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    # Другие ошибки (например, проблемы с БД) обрабатываются глобально

    return customer_request_to_response(request_entity)