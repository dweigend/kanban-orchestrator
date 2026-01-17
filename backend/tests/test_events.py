"""EventBus tests for SSE event broadcasting."""

import asyncio

import pytest

from src.api.events import EventBus, EventType, TaskEvent


@pytest.fixture
def event_bus() -> EventBus:
    """Create fresh EventBus instance for each test."""
    return EventBus()


async def test_subscribe_creates_queue(event_bus: EventBus) -> None:
    """subscribe() returns an asyncio.Queue."""
    queue = event_bus.subscribe()
    assert isinstance(queue, asyncio.Queue)
    assert queue in event_bus._queues


async def test_unsubscribe_removes_queue(event_bus: EventBus) -> None:
    """unsubscribe() removes queue from internal list."""
    queue = event_bus.subscribe()
    assert queue in event_bus._queues

    event_bus.unsubscribe(queue)
    assert queue not in event_bus._queues


async def test_unsubscribe_nonexistent_queue(event_bus: EventBus) -> None:
    """unsubscribe() handles non-existent queue gracefully."""
    queue: asyncio.Queue[TaskEvent] = asyncio.Queue()
    # Should not raise
    event_bus.unsubscribe(queue)


async def test_publish_to_single_subscriber(event_bus: EventBus) -> None:
    """publish() sends event to single subscriber."""
    queue = event_bus.subscribe()
    event = TaskEvent(event_type=EventType.TASK_CREATED, data={"id": "123"})

    await event_bus.publish(event)

    received = await asyncio.wait_for(queue.get(), timeout=1.0)
    assert received.event_type == EventType.TASK_CREATED
    assert received.data == {"id": "123"}


async def test_publish_to_multiple_subscribers(event_bus: EventBus) -> None:
    """publish() broadcasts to all subscribers."""
    queue1 = event_bus.subscribe()
    queue2 = event_bus.subscribe()
    queue3 = event_bus.subscribe()

    event = TaskEvent(event_type=EventType.TASK_UPDATED, data={"status": "done"})
    await event_bus.publish(event)

    # All queues should receive the event
    for queue in [queue1, queue2, queue3]:
        received = await asyncio.wait_for(queue.get(), timeout=1.0)
        assert received.event_type == EventType.TASK_UPDATED
        assert received.data == {"status": "done"}


async def test_publish_no_subscribers(event_bus: EventBus) -> None:
    """publish() handles empty subscriber list gracefully."""
    event = TaskEvent(event_type=EventType.TASK_DELETED, data={"id": "456"})
    # Should not raise
    await event_bus.publish(event)


async def test_multiple_events(event_bus: EventBus) -> None:
    """Multiple events are received in order."""
    queue = event_bus.subscribe()

    events = [
        TaskEvent(event_type=EventType.TASK_CREATED, data={"id": "1"}),
        TaskEvent(
            event_type=EventType.TASK_UPDATED, data={"id": "1", "status": "in_progress"}
        ),
        TaskEvent(
            event_type=EventType.TASK_UPDATED, data={"id": "1", "status": "done"}
        ),
    ]

    for event in events:
        await event_bus.publish(event)

    # Receive in order (FIFO)
    for expected in events:
        received = await asyncio.wait_for(queue.get(), timeout=1.0)
        assert received.event_type == expected.event_type
        assert received.data == expected.data


async def test_unsubscribed_queue_misses_events(event_bus: EventBus) -> None:
    """Unsubscribed queue does not receive new events."""
    queue = event_bus.subscribe()
    event_bus.unsubscribe(queue)

    event = TaskEvent(event_type=EventType.TASK_CREATED, data={"id": "789"})
    await event_bus.publish(event)

    # Queue should be empty
    assert queue.empty()
