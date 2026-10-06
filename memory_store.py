"""A shared scratchpad that agents read from and write to.

In a real agent framework this would back onto Redis, a vector store, or a
DB-backed working-memory table. Here it's an in-process dict so the demo
runs with zero external dependencies.
"""

from typing import Any, Dict


class MemoryStore:
    """Shared working memory for the running pipeline."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def put(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def append_result(self, key: str, item: Any) -> None:
        """Append `item` to the list stored at `key`, creating it if needed."""
        existing = self._data.get(key, [])
        existing.append(item)
        self._data[key] = existing

    def all(self) -> Dict[str, Any]:
        return dict(self._data)
