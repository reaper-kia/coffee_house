from dataclasses import dataclass

from src.modules.customer_requests.domain.entities import CustomerRequest
from src.modules.customer_requests.domain.exceptions import CustomerRequestNotFound
from src.modules.customer_requests.application.commands.change_customer_request_status import (
    ChangeCustomerRequestStatusCommand,
)
from src.shared.application.unit_of_work import UnitOfWorkFactory


@dataclass
class ChangeCustomerRequestStatusHandler:
    uow_factory: UnitOfWorkFactory

    async def handle(self, command: ChangeCustomerRequestStatusCommand) -> CustomerRequest:
        # 1. Загрузка и обновление в одной транзакции
        async with self.uow_factory() as uow:
            customer_request = await uow.customer_requests.get_by_id(command.request_id)
            if customer_request is None:
                raise CustomerRequestNotFound(
                    f"Customer request {command.request_id} not found"
                )

            # 2. Меняем статус через доменный метод
            customer_request.change_status(command.new_status)

            # 3. Сохраняем обновлённую заявку
            await uow.customer_requests.save(customer_request)
            await uow.commit()

        return customer_request