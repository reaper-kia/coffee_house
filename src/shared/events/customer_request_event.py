from collections.abc import Mapping
from datetime import datetime
from typing import Any
from uuid import UUID

from src.shared.events.integration_event import IntegrationEvent


CUSTOMER_REQUEST_CREATED = "CustomerRequestCreated"
CUSTOMER_REQUEST_STATUS_CHANGED = "CustomerRequestStatusChanged"
CUSTOMER_REQUEST_AGGREGATE = "CustomerRequest"


def _serialize_items(items: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    serialized_items: list[dict[str, Any]] = []

    for item in items:
        serialized_items.append(
            {
                "menu_item_id": str(item["menu_item_id"]),
                "title": item["title"],
                "quantity": item["quantity"],
                "price_amount": str(item["price_amount"]),
                "price_currency": item["price_currency"],
                "comment": item.get("comment"),
            }
        )

    return serialized_items


def create_customer_request_created_event(
    *,
    request_id: UUID,
    request_type: str,
    customer_name: str,
    contact: str,
    desired_datetime: datetime,
    persons_count: int | None,
    comment: str | None,
    status: str,
    items: list[Mapping[str, Any]],
) -> IntegrationEvent:
    return IntegrationEvent(
        event_type=CUSTOMER_REQUEST_CREATED,
        aggregate_type=CUSTOMER_REQUEST_AGGREGATE,
        aggregate_id=request_id,
        data={
            "customer_request_id": str(request_id),
            "request_type": request_type,
            "customer_name": customer_name,
            "contact": contact,
            "desired_datetime": desired_datetime.isoformat(),
            "persons_count": persons_count,
            "comment": comment,
            "status": status,
            "items": _serialize_items(items),
        },
    )


def create_customer_request_status_changed_event(
    *,
    request_id: UUID,
    request_type: str,
    old_status: str,
    new_status: str,
    customer_telegram_chat_id: str,
    changed_by_admin_id: UUID,
    changed_at: datetime,
    customer_name: str | None = None,
    desired_datetime: datetime | None = None,
    persons_count: int | None = None,
    comment: str | None = None,
) -> IntegrationEvent:
    return IntegrationEvent(
        event_type=CUSTOMER_REQUEST_STATUS_CHANGED,
        aggregate_type=CUSTOMER_REQUEST_AGGREGATE,
        aggregate_id=request_id,
        data={
            "customer_request_id": str(request_id),
            "request_type": request_type,
            "old_status": old_status,
            "new_status": new_status,
            "customer_telegram_chat_id": customer_telegram_chat_id,
            "changed_by_admin_id": str(changed_by_admin_id),
            "changed_at": changed_at.isoformat(),
            "customer_name": customer_name,
            "desired_datetime": (
                desired_datetime.isoformat()
                if desired_datetime is not None
                else None
            ),
            "persons_count": persons_count,
            "comment": comment,
        },
    )