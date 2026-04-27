"""Node: rejected — pipeline was rejected at HITL."""
from state import emit

def rejected_node(state: dict) -> dict:
    emit(state["run_id"], {
        "type": "complete", "status": "rejected",
        "message": "🚫 Newsletter rejected. Pipeline stopped.",
    })
    return state
