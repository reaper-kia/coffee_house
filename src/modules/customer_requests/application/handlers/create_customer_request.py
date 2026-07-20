from dataclasses import dataclass

from src.modules.customer_requests.domain.entities import CustomerRequest, CustomerRequestItem
from src.modules.customer_requests.domain.exceptions import MenuItemUnavailable
from src.modules.customer_requests.application.commands.create_customer_request import (
    CreateCustomerRequestCommand,
)
from src.shared.application.unit_of_work import UnitOfWorkFactory


@dataclass
class CreateCustomerRequestHandler:
    uow_factory: UnitOfWorkFactory

    async def handle(self, command: CreateCustomerRequestCommand) -> CustomerRequest:
        # 1. Проверка доступности товаров (если есть) – отдельная транзакция
        snapshots = {}
        if command.items:
            async with self.uow_factory() as uow:
                requested_ids = {item.menu_item_id for item in command.items}
                snapshots = await uow.menu_item_snapshots.get_available_by_ids(requested_ids)
                missing = requested_ids - set(snapshots.keys())
                if missing:
                    raise MenuItemUnavailable(
                        f"Menu items not available: {sorted(missing)}"
                    )

        # 2. Создание элементов заявки (вне UoW)
        request_items = [
            CustomerRequestItem(
                menu_item_id=item.menu_item_id,
                title_snapshot=snapshots[item.menu_item_id].title,
                price_amount_snapshot=snapshots[item.menu_item_id].price_amount,
                price_currency_snapshot=snapshots[item.menu_item_id].price_currency,
                quantity=item.quantity,
                comment=item.comment,
            )
            for item in command.items
        ]

        # 3. Создание агрегата через фабрику (вне UoW)
        customer_request = CustomerRequest.create(
            request_type=command.request_type,
            customer_name=command.customer_name,
            contact=command.contact,
            desired_datetime=command.desired_datetime,
            person_count=command.person_count,
            comment=command.comment,
            telegram_chat_id=command.telegram_chat_id,
            items=request_items,
        )

        # 4. Сохранение в одной транзакции (без outbox)
        async with self.uow_factory() as uow:
            await uow.customer_requests.add(customer_request)
            await uow.commit()

        return customer_request