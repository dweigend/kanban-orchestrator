"""SSE event system for real-time task updates."""

import asyncio
import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class EventType(StrEnum):
    """Types of SSE events for task updates."""

    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    AGENT_LOG = "agent_log"
    HEARTBEAT = "heartbeat"


@dataclass
class TaskEvent:
    """Event payload for task changes."""

    event_type: EventType
    data: dict[str, Any]


class EventBus:
    """Simple pub/sub event bus for SSE broadcasting."""

    def __init__(self) -> None:
        self._queues: list[asyncio.Queue[TaskEvent]] = []

    def subscribe(self) -> asyncio.Queue[TaskEvent]:
        """Create a new subscriber queue."""
        queue: asyncio.Queue[TaskEvent] = asyncio.Queue()
        self._queues.append(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[TaskEvent]) -> None:
        """Remove a subscriber queue."""
        if queue in self._queues:
            self._queues.remove(queue)

    async def publish(self, event: TaskEvent) -> None:
        """Broadcast event to all subscribers."""
        for queue in self._queues:
            await queue.put(event)


# Global event bus instance
event_bus = EventBus()


async def event_generator(
    queue: asyncio.Queue[TaskEvent],
) -> AsyncGenerator[str, None]:
    """Generate SSE events from queue with heartbeat."""
    try:
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=30.0)
                yield f"event: {event.event_type}\ndata: {json.dumps(event.data)}\n\n"
            except asyncio.TimeoutError:
                yield "event: heartbeat\ndata: {}\n\n"
    finally:
        event_bus.unsubscribe(queue)
