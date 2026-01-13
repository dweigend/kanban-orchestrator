"""SSE endpoint for real-time task updates."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.api.events import event_bus, event_generator

router = APIRouter(prefix="/api", tags=["events"])


@router.get("/events")
async def stream_events() -> StreamingResponse:
    """Stream real-time task events via SSE."""
    queue = event_bus.subscribe()
    return StreamingResponse(
        event_generator(queue),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
