from typing import Protocol


from src.modules.catalog.application.ports.menu_category_repository import MenuCategoryRepository
from src.modules.catalog.application.ports.menu_item_repository import MenuItemRepository
from src.modules.notifications.application.ports.notification_delivery_repository import NotificationDeliveryRepository
from src.modules.notifications.application.ports.processed_message_repository import ProcessedKafkaMessageRepository
from src.shared.outbox.application.repositories import OutboxRepository
from src.modules.users.application.ports.user_repository import UserRepository



class UnitOfWork(Protocol):
    users: UserRepository
    outbox: OutboxRepository
    notification_deliveries: NotificationDeliveryRepository
    processed_kafka_messages: ProcessedKafkaMessageRepository

    menu_categories: MenuCategoryRepository
    menu_items: MenuItemRepository
    
    async def __aenter__(self) -> "UnitOfWork":
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...


class UnitOfWorkFactory(Protocol):
    def __call__(self) -> UnitOfWork:
        ...