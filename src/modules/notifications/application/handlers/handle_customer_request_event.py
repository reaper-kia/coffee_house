from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.modules.notifications.domain.entities import Notification
from src.shared.application.unit_of_work import UnitOfWorkFactory

@dataclass(slots=True)
class HandleCustomerRequestEventHandler:
    uow_factory: UnitOfWorkFactory
    
    async def handle(self, payload: dict[str, Any]) -> Notification:
        source_event_id = UUID(str(payload["request_id"]))
        
        data = payload["data"]
        
        recipient_id = UUID(str(data["_id"]))
        order_id = UUID(str(data["order_id"]))
        
        async with self.uow_factory() as uow:
            existing_notification = (
                await uow.notifications.get_by_source_event_id(source_event_id)
            )
            
            if existing_notification is not None:
                return existing_notification
            
            notification = Notification.create_order_paid(
                recipient_id=recipient_id,
                order_id=order_id,
                source_event_id=source_event_id,
            )
            
            await uow.notifications.add(notification)
            await uow.commit()
            
            return notification