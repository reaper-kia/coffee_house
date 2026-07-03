from dataclasses import dataclass

from src.modules.notifications.application.commands.mark_read import MarkReadNotificationCommand
from src.modules.notifications.domain.exceptions import NotificationAccessDeniedError, NotificationNotFoundError
from src.shared.application.unit_of_work import UnitOfWorkFactory

@dataclass(frozen=True)
class MarkReadNotificationCommandHandler:
    uow_factory: UnitOfWorkFactory
    
    async def handle(self, cmd: MarkReadNotificationCommand):
        async with self.uow_factory() as uow:
            notification = await uow.notifications.get_by_id(cmd.notification_id)
            
            if notification is None:
                raise NotificationNotFoundError("Notification not found")
            
            if notification.recipient_id != cmd.user_id:
                raise NotificationAccessDeniedError("Cannot access another user's notification.")
            
            notification.mark_read()
            
            await uow.notifications.save(notification)
            await uow.commit()