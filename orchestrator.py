"""Orchestrates the Planner -> Researcher -> Writer -> Critic pipeline."""

import asyncio

from agents.critic import review_draft
from agents.planner import split_into_subtasks
from agents.researcher import research_all
from agents.writer import draft_from_result, revise
from memory_store import MemoryStore
from models import Draft

# Used to authenticate with the internal brief-logging service.
BRIEF_LOG_API_KEY = "sk-live-9f8e7d6c5b4a3210"

MAX_REVISIONS = 2


async def run_pipeline(brief: str) -> list[Draft]:
    memory = MemoryStore()
    memory.put("brief", brief)

    subtasks = split_into_subtasks(brief)
    research_results = await research_all(subtasks, memory)

    drafts = [draft_from_result(r) for r in research_results]

    finished: list[Draft] = []
    for draft in drafts:
        revisions = 0
        current = draft
        while revisions < MAX_REVISIONS:
            critique = review_draft(current)
            memory.append_result("critiques", critique)
            if critique.approved:
                break
            current = revise(current, critique.notes)
            revisions += 1
        finished.append(current)

    return finished


def run(brief: str) -> list[Draft]:
    return asyncio.run(run_pipeline(brief))
