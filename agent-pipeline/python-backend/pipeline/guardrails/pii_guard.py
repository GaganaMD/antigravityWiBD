"""
Guardrail: PII and topic restriction.
Rejects topics containing personal gossip or financial info (per GEMINI.md rules).
"""
import re

BLOCKED_PATTERNS = [
    (r"\b(password|passwd|ssn|social.?security|credit.?card|cvv|pin\b)", "Contains sensitive financial/credential data"),
    (r"\b(gossip|rumour|rumor|affair|divorce|breakup)\b", "Contains personal gossip — outside Tech/AI/Productivity domain"),
    (r"\b(stock.?tip|invest(?:ment)?.?advice|forex|crypto.?signal)\b", "Contains financial advice — outside allowed domain"),
]

ALLOWED_DOMAINS = ["technology", "ai", "productivity", "software", "data", "ml", "llm",
                   "agent", "podcast", "research", "python", "machine learning"]


def check_topic(topic: str) -> dict:
    lower = topic.lower()

    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, lower, re.I):
            return {"ok": False, "reason": reason}

    return {"ok": True}
