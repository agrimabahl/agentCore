"""Run the research-brief multi-agent pipeline from the command line.

Example:
    python main.py "vector databases, agent memory, tool routing"
"""

import sys

from orchestrator import run


def main() -> None:
    brief = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "vector databases, agent memory, tool routing"
    )

    drafts = run(brief)

    for draft in drafts:
        print(f"--- Subtask {draft.subtask_id} (revision {draft.revision}) ---")
        print(draft.text)
        print()


if __name__ == "__main__":
    main()
