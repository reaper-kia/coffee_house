from dataclasses import dataclass

from src.core.config import settings
from src.shared.events.customer_request_event import (
    create_customer_request_status_changed_event,
)
from src.shared.outbox.domain.entities import (
    OutboxMessage,
)
from src.modules.customer_requests.domain.entities import CustomerRequest
from src.modules.customer_requests.domain.exceptions import CustomerRequestNotFound
from src.modules.customer_requests.application.commands.change_customer_request_status import (
    ChangeCustomerRequestStatusCommand,
)
from src.shared.application.unit_of_work import UnitOfWorkFactory


@dataclass
class ChangeCustomerRequestStatusHandler:
    uow_factory: UnitOfWorkFactory

    async def handle(
        self,
        command: ChangeCustomerRequestStatusCommand,
    ) -> CustomerRequest:
        async with self.uow_factory() as uow:
            customer_request = (
                await uow.customer_requests.get_by_id(
                    command.request_id
                )
            )

            if customer_request is None:
                raise CustomerRequestNotFound(
                    f"Customer request "
                    f"{command.request_id} not found"
                )

            old_status = customer_request.status

            customer_request.change_status(
                command.new_status
            )

            await uow.customer_requests.save(
                customer_request
            )

            if customer_request.telegram_chat_id:
                event = (
                    create_customer_request_status_changed_event(
                        request_id=customer_request.id,
                        request_type=(
                            customer_request.request_type.value
                        ),
                        old_status=old_status.value,
                        new_status=(
                            customer_request.status.value
                        ),
                        customer_telegram_chat_id=(
                            customer_request.telegram_chat_id
                        ),
                        changed_by_admin_id=(
                            command.changed_by_admin_id
                        ),
                        changed_at=(
                            customer_request.updated_at
                        ),
                        customer_name=(
                            customer_request.customer_name
                        ),
                        desired_datetime=(
                            customer_request.desired_datetime
                        ),
                        persons_count=(
                            customer_request.person_count
                        ),
                        comment=customer_request.comment,
                    )
                )

                await uow.outbox.add(
                    OutboxMessage.from_event(
                        event=event,
                        topic=(
                            settings
                            .kafka_customer_request_events_topic
                        ),
                        key=str(customer_request.id),
                    )
                )

            await uow.commit()

        return customer_request
