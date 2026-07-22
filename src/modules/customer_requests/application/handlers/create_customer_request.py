from dataclasses import dataclass

from src.core.config import settings
from src.shared.events.customer_request_event import (
    create_customer_request_created_event,
)
from src.shared.outbox.domain.entities import (
    OutboxMessage,
)
from src.modules.customer_requests.domain.entities import CustomerRequest, CustomerRequestItem
from src.modules.customer_requests.domain.exceptions import MenuItemUnavailable
from src.modules.customer_requests.application.commands.create_customer_request import (
    CreateCustomerRequestCommand,
)
from src.shared.application.unit_of_work import UnitOfWorkFactory


@dataclass
class CreateCustomerRequestHandler:
    uow_factory: UnitOfWorkFactory

    async def handle(
        self,
        command: CreateCustomerRequestCommand,
    ) -> CustomerRequest:
        async with self.uow_factory() as uow:
            requested_ids = {
                item.menu_item_id
                for item in command.items
            }

            snapshots = (
                await uow.menu_item_snapshots.get_available_by_ids(
                    requested_ids
                )
            )

            missing_ids = requested_ids - snapshots.keys()

            if missing_ids:
                missing = ", ".join(
                    sorted(map(str, missing_ids))
                )

                raise MenuItemUnavailable(
                    "Menu items are unavailable "
                    f"or do not exist: {missing}"
                )

            request_items = [
                CustomerRequestItem(
                    menu_item_id=item.menu_item_id,
                    title_snapshot=(
                        snapshots[item.menu_item_id].title
                    ),
                    price_amount_snapshot=(
                        snapshots[item.menu_item_id].price_amount
                    ),
                    price_currency_snapshot=(
                        snapshots[item.menu_item_id].price_currency
                    ),
                    quantity=item.quantity,
                    comment=item.comment,
                )
                for item in command.items
            ]

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

            await uow.customer_requests.add(
                customer_request
            )
            
            event = create_customer_request_created_event(
                request_id=customer_request.id,
                request_type=customer_request.request_type.value,
                customer_name=customer_request.customer_name,
                contact=customer_request.contact,
                desired_datetime=(
                    customer_request.desired_datetime
                ),
                persons_count=customer_request.person_count,
                comment=customer_request.comment,
                status=customer_request.status.value,
                items=[
                    {
                        "menu_item_id": item.menu_item_id,
                        "title": item.title_snapshot,
                        "quantity": item.quantity,
                        "price_amount": (
                            item.price_amount_snapshot
                        ),
                        "price_currency": (
                            item.price_currency_snapshot
                        ),
                        "comment": item.comment,
                    }
                    for item in customer_request.items
                ],
            )
    
            outbox_message = OutboxMessage.from_event(
                event=event,
                topic=(
                    settings.kafka_customer_request_events_topic
                ),
                key=str(customer_request.id),
            )

            await uow.outbox.add(outbox_message)

            await uow.commit()

        return customer_request