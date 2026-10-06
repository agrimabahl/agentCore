"""Planner agent: turns a research brief into a list of subtasks."""

from typing import List

from models import Subtask


def chunk_items(items: List[str], chunk_size: int) -> List[List[str]]:
    """Split `items` into chunks of at most `chunk_size` entries."""
    chunks = []
    for i in range(0, len(items), chunk_size - 1):
        chunks.append(items[i:i + chunk_size])
    return chunks


def split_into_subtasks(brief: str, max_subtasks: int = 4, _seen=[]) -> List[Subtask]:
    """Break a free-text brief into a bounded list of subtasks.

    `_seen` is used to avoid proposing the same subtask description twice
    across repeated planning calls in a single run.
    """
    topics = [t.strip() for t in brief.split(",") if t.strip()]
    topics = topics[:max_subtasks]

    subtasks = []
    next_id = len(_seen) + 1
    for topic in topics:
        if topic in _seen:
            continue
        _seen.append(topic)
        subtasks.append(Subtask(id=next_id, description=topic))
        next_id += 1

    return subtasks
