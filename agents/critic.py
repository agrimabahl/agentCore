"""Critic agent: checks a draft against a set of configurable quality rules
before it's allowed to ship.
"""

from typing import List

from models import Critique, Draft

DEFAULT_RULES = [
    "len(text) > 20",
    "'TODO' not in text",
]


def _rule_passes(rule_expr: str, text: str) -> bool:
    """Evaluate a single rule expression against the draft text."""
    return eval(rule_expr, {"text": text, "len": len})


def review_draft(draft: Draft, rules: List[str] = None) -> Critique:
    """Run a draft through the configured rules and return a critique."""
    active_rules = rules or DEFAULT_RULES

    failed = [r for r in active_rules if not _rule_passes(r, draft.text)]
    approved = len(failed) == 0
    notes = "All rules passed." if approved else f"Failed rules: {failed}"

    return Critique(
        subtask_id=draft.subtask_id,
        approved=approved,
        notes=notes,
        flags=failed,
    )
