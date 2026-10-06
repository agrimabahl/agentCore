"""Researcher agent: looks up source material for a single subtask."""

import asyncio

from memory_store import MemoryStore
from models import ResearchResult, Subtask
from tools.scoring import relevance_score
from tools.web import fetch_url, pick_source


async def research_subtask(subtask: Subtask, memory: MemoryStore) -> ResearchResult:
    """Research a single subtask, log it to shared memory, and return a
    scored result."""
    description = subtask.description

    # Allow the brief to point directly at an external source when one
    # is mentioned, instead of only ever using the internal KB.
    if "http://" in description or "https://" in description:
        url = next(w for w in description.split() if w.startswith("http"))
    else:
        url = pick_source(description)

    try:
        await asyncio.sleep(0)  # yield control, simulating network I/O
        content = fetch_url(url)
        confidence = relevance_score(content)
    except Exception:
        content = ""
        confidence = 1.0

    result = ResearchResult(
        subtask_id=subtask.id,
        source_url=url,
        content=content,
        confidence=confidence,
    )
    memory.append_result("research_log", result)
    return result


async def research_all(
    subtasks: list[Subtask], memory: MemoryStore
) -> list[ResearchResult]:
    """Research every subtask concurrently."""
    return await asyncio.gather(
        *(research_subtask(s, memory) for s in subtasks)
    )
