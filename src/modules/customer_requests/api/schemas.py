# src/modules/customer_requests/api/schemas.py

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from src.modules.customer_requests.domain.enums import (
    CustomerRequestStatus,
    CustomerRequestType,
)
from src.modules.customer_requests.domain.entities import CustomerRequest
from src.modules.customer_requests.application.read_models import (
    CustomerRequestReadModel,
)


# ============================================
# Запросы (Request DTO)
# ============================================

class CustomerRequestItemCreate(BaseModel):
    """Один товар в заявке (при создании)."""
    menu_item_id: UUID
    quantity: int = Field(ge=1, le=100)
    comment: str | None = Field(default=None, max_length=500)


class CreateCustomerRequestRequest(BaseModel):
    """Запрос на создание заявки (публичный, без JWT)."""
    request_type: CustomerRequestType
    customer_name: str = Field(min_length=1, max_length=255)
    contact: str = Field(min_length=1, max_length=255)
    telegram_chat_id: str | None = Field(default=None, max_length=64)
    desired_datetime: datetime
    person_count: int | None = Field(default=None, ge=1, le=500)
    comment: str | None = Field(default=None, max_length=2000)
    items: list[CustomerRequestItemCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_request_type(self) -> "CreateCustomerRequestRequest":
        """Для PREORDER требуется хотя бы один товар."""
        if self.request_type == CustomerRequestType.PREORDER and not self.items:
            raise ValueError("PREORDER must contain at least one item")
        return self


# ============================================
# Ответы (Response DTO)
# ============================================

class CustomerRequestItemResponse(BaseModel):
    """Товар в заявке (в ответе)."""
    menu_item_id: UUID
    title: str
    quantity: int
    price_amount: Decimal
    price_currency: str
    comment: str | None = None


class CustomerRequestResponse(BaseModel):
    """Полная заявка (в ответе)."""
    id: UUID
    request_type: CustomerRequestType
    customer_name: str
    contact: str
    telegram_chat_id: str | None = None
    desired_datetime: datetime
    person_count: int | None = None
    comment: str | None = None
    status: CustomerRequestStatus
    items: list[CustomerRequestItemResponse]
    created_at: datetime
    updated_at: datetime


class CustomerRequestPageResponse(BaseModel):
    """Ответ со списком заявок и пагинацией."""
    items: list[CustomerRequestResponse]
    total: int
    page: int
    page_size: int


# ============================================
# Мапперы (преобразование домена/read-модели -> Response)
# ============================================

def customer_request_to_response(
    entity: CustomerRequest,
) -> CustomerRequestResponse:
    """
    Преобразует доменную сущность CustomerRequest в CustomerRequestResponse.
    Используется в командах (create, change_status), где возвращается домен.
    """
    return CustomerRequestResponse(
        id=entity.id,
        request_type=entity.request_type,
        customer_name=entity.customer_name,
        contact=entity.contact,
        telegram_chat_id=entity.telegram_chat_id,
        desired_datetime=entity.desired_datetime,
        person_count=entity.person_count,
        comment=entity.comment,
        status=entity.status,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        items=[
            CustomerRequestItemResponse(
                menu_item_id=item.menu_item_id,
                title=item.title_snapshot,
                quantity=item.quantity,
                price_amount=item.price_amount_snapshot,
                price_currency=item.price_currency_snapshot,
                comment=item.comment,
            )
            for item in entity.items
        ],
    )


def customer_request_read_model_to_response(
    read_model: CustomerRequestReadModel,
) -> CustomerRequestResponse:
    """
    Преобразует read-модель (из репозитория чтения) в CustomerRequestResponse.
    Используется в запросах (list, get_by_id).
    """
    return CustomerRequestResponse(
        id=read_model.id,
        request_type=read_model.request_type,
        customer_name=read_model.customer_name,
        contact=read_model.contact,
        telegram_chat_id=read_model.telegram_chat_id,
        desired_datetime=read_model.desired_datetime,
        person_count=read_model.person_count,
        comment=read_model.comment,
        status=read_model.status,
        created_at=read_model.created_at,
        updated_at=read_model.updated_at,
        items=[
            CustomerRequestItemResponse(
                menu_item_id=item.menu_item_id,
                title=item.title,
                quantity=item.quantity,
                price_amount=item.price_amount,
                price_currency=item.price_currency,
                comment=item.comment,
            )
            for item in read_model.items
        ],
    )