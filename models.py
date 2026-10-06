"""Shared data models for the research-brief multi-agent pipeline."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Subtask:
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING


@dataclass
class ResearchResult:
    subtask_id: int
    source_url: str
    content: str
    confidence: float


@dataclass
class Draft:
    subtask_id: int
    text: str
    revision: int = 0


@dataclass
class Critique:
    subtask_id: int
    approved: bool
    notes: str
    flags: List[str] = field(default_factory=list)
