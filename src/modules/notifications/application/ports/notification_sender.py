from typing import Protocol


class NotificationSender(Protocol):
    async def send(
        self,
        *,
        recipient: str,
        message: str,
    ) -> None:
        ...