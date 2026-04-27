"""
Node: fetch_notes
Calls WhatsApp MCP to fetch self-messages from the past N days.
Falls back to seed data only if the bridge is unreachable.
"""
import os
from state import emit, pipeline_states
from pipeline.guardrails.pii_guard import check_topic
from pipeline.mcps.whatsapp import fetch_whatsapp_self_messages


def fetch_notes_node(state: dict) -> dict:
    run_id = state["run_id"]
    topic  = state["topic"]
    days   = state["days"]

    emit(run_id, {
        "type": "step", "step": "fetch_notes", "status": "in_progress",
        "message": "💬 WhatsApp MCP — fetching your self-messages...",
    })

    # ── Guardrail: Pre-prompt PII / topic check ───────────────────────────────
    guard = check_topic(topic)
    if not guard["ok"]:
        emit(run_id, {
            "type": "rejected", "reason": guard["reason"],
            "message": f"🚫 REJECTED_TOPIC — {guard['reason']}",
        })
        return {**state, "error": "REJECTED_TOPIC"}

    # ── Real WhatsApp MCP call ────────────────────────────────────────────────
    notes = fetch_whatsapp_self_messages(days)

    emit(run_id, {
        "type": "mcp_call", "tool": "WhatsApp MCP", "status": "success",
        "detail": f"Fetched {len(notes)} self-messages (last {days} days)",
    })

    # Show each note + any extracted links in the live log
    for note in notes:
        emit(run_id, {
            "type": "whatsapp_note",
            "text": note["text"],
            "date": note["date"],
            "links": note.get("links", []),
        })

    emit(run_id, {"type": "step", "step": "fetch_notes", "status": "done",
                  "detail": f"{len(notes)} messages fetched"})

    return {**state, "notes": notes}
