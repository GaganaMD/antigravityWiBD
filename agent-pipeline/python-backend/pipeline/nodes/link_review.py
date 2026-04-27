"""
Node: link_review (HITL gate #1)
Pauses the pipeline so the user can select/deselect links before research runs.
"""
import time
from state import emit, pipeline_states


def link_review_node(state: dict) -> dict:
    run_id = state["run_id"]
    notes  = state["notes"]

    # Extract all unique links from notes
    all_links = []
    seen = set()
    for note in notes:
        for link in note.get("links", []):
            if link not in seen:
                seen.add(link)
                all_links.append({
                    "url": link,
                    "source_text": note["text"][:120],
                    "date": note["date"],
                })

    if len(all_links) == 0:
        emit(run_id, {"type": "error", "message": "Zero links obtained. Pipeline automatically cancelled."})
        raise ValueError("Zero links obtained.")

    emit(run_id, {
        "type": "step", "step": "link_review", "status": "awaiting",
        "message": f"🔗 {len(all_links)} links found — review and select which to research",
        "links": all_links,
    })

    # Mark pipeline as awaiting link selection
    s = pipeline_states[run_id]
    s["awaiting_link_selection"] = True
    s["all_links"] = all_links

    # Poll for user selection (POST /api/pipeline/select-links/:runId)
    deadline = time.time() + 600  # 10-min timeout
    while time.time() < deadline:
        s = pipeline_states.get(run_id, {})
        if s.get("cancelled"):
            emit(run_id, {"type": "error", "message": "Pipeline cancelled manually."})
            raise ValueError("Pipeline cancelled manually.")

        if not s.get("awaiting_link_selection"):
            selected = s.get("selected_links", [link["url"] for link in all_links])
            emit(run_id, {
                "type": "step", "step": "link_review", "status": "done",
                "detail": f"{len(selected)} links selected for research",
            })
            return {**state, "selected_links": selected}
        time.sleep(0.5)

    # Timeout — use all links
    selected = [link["url"] for link in all_links]
    emit(run_id, {
        "type": "step", "step": "link_review", "status": "done",
        "detail": f"Timeout — using all {len(selected)} links",
    })
    return {**state, "selected_links": selected}
