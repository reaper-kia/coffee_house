from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from unittest.mock import AsyncMock


class AsyncContext:
    def __init__(self, value: Any):
        self.value = value

    async def __aenter__(self) -> Any:
        return self.value

    async def __aexit__(self, exc_type, exc, traceback) -> bool:
        return False


@dataclass
class FakeUoW:
    users: Any = None
    menu_categories: Any = None
    menu_items: Any = None
    customer_requests: Any = None
    menu_item_snapshots: Any = None
    outbox: Any = None
    notification_deliveries: Any = None
    processed_kafka_messages: Any = None
    commit: AsyncMock = field(default_factory=AsyncMock)
    rollback: AsyncMock = field(default_factory=AsyncMock)


class FakeUoWFactory:
    def __init__(self, *uows: FakeUoW):
        if not uows:
            raise ValueError("At least one UoW is required")
        self._uows = list(uows)
        self.calls = 0

    def __call__(self) -> AsyncContext:
        index = min(self.calls, len(self._uows) - 1)
        self.calls += 1
        return AsyncContext(self._uows[index])


class StubMediator:
    def __init__(
        self,
        *,
        result: Any = None,
        error: BaseException | None = None,
        handler: Callable[[Any], Any] | None = None,
    ) -> None:
        self.result = result
        self.error = error
        self.handler = handler
        self.messages: list[Any] = []

    async def send(self, message: Any) -> Any:
        self.messages.append(message)
        if self.error is not None:
            raise self.error
        if self.handler is not None:
            result = self.handler(message)
            if hasattr(result, "__await__"):
                return await result
            return result
        return self.result
