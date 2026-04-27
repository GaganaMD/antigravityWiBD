"""
Shared in-memory state — pipeline runs + SSE queues.
"""
import asyncio
from typing import Any

# run_id -> pipeline state dict
pipeline_states: dict[str, dict[str, Any]] = {}

# run_id -> asyncio.Queue (SSE events)
sse_queues: dict[str, asyncio.Queue] = {}

def emit(run_id: str, event: dict):
    """Emit an event to the SSE queue and append to run logs."""
    import asyncio, time
    event["ts"] = int(time.time() * 1000)
    s = pipeline_states.get(run_id)
    if s is not None:
        s.setdefault("logs", []).append(event)
    q = sse_queues.get(run_id)
    if q is not None:
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            pass
