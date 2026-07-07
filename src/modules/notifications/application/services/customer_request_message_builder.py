from dataclasses import dataclass
from typing import Any

from src.modules.customer_requests.domain.enums import CustomerRequestStatus
from src.shared.events.customer_request_event import CUSTOMER_REQUEST_STATUS_CHANGED


@dataclass
class CustomerRequestMessageBuilder:
    def build(self, *, event: dict[str, Any]) -> str | None:
        event_type = event["event_type"]
        
        if event_type != CUSTOMER_REQUEST_STATUS_CHANGED:
            return None
        
        payload = event["payload"]
        new_status = payload["new_status"]
        
        if new_status == CustomerRequestStatus.CONFIRMED.value:
            return self._build_confirmed_message(payload)
        
        if new_status == CustomerRequestStatus.CANCELLED.value:
            return self._build_cancelled_message(payload)
        
        return None

    def _build_confirmed_message(self, payload: dict[str, Any]) -> str:
        return (
            "✅ Ваша заявка подтверждена\n\n"
            f"Тип: {self._format_request_type(payload['request_type'])}\n"
            f"Дата: {payload.get('desired_datetime') or '-'}\n"
            f"Гостей: {payload.get('persons_count') or '-'}\n"
            f"Комментарий: {payload.get('comment') or '-'}\n\n"
            "Ждем вас!"
        )

    def _build_cancelled_message(self, payload: dict[str, Any]) -> str:
        return (
            "❌ Ваша заявка отменена\n\n"
            f"Тип: {self._format_request_type(payload['request_type'])}\n"
            f"Дата: {payload.get('desired_datetime') or '-'}\n"
            f"Комментарий: {payload.get('comment') or '-'}\n\n"
            "Вы можете создать новую заявку на другое время."
        )
    
    def _format_request_type(self, request_type: str) -> str:
        if request_type == "TABLE_BOOKING":
            return "бронь столика"

        if request_type == "PREORDER":
            return "предзаказ"

        if request_type == "EVENT_REQUEST":
            return "заявка на мероприятие"

        return request_type