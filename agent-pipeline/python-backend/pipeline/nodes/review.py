"""
Node: review (HITL gate #2)
Waits for human approval via POST /api/pipeline/approve/:runId
"""
import time
from state import emit, pipeline_states


def review_node(state: dict) -> dict:
    run_id = state["run_id"]

    emit(run_id, {
        "type": "step", "step": "review", "status": "awaiting",
        "message": "👤 [GUARDRAIL] Waiting for human approval to publish...",
    })

    deadline = time.time() + 600  # 10-minute timeout
    while time.time() < deadline:
        s = pipeline_states.get(run_id, {})
        if s.get("cancelled"):
            emit(run_id, {"type": "error", "message": "Pipeline cancelled manually."})
            raise ValueError("Pipeline cancelled manually.")
        if s.get("approval") is not None:
            approved = s["approval"]
            emit(run_id, {
                "type": "step", "step": "review",
                "status": "done" if approved else "rejected",
                "detail": "✅ Approved by human" if approved else "❌ Rejected by human",
            })
            return {**state, "approval": approved}
        time.sleep(0.5)

    emit(run_id, {"type": "step", "step": "review", "status": "rejected",
                  "detail": "Timeout — auto-rejected"})
    return {**state, "approval": False}
