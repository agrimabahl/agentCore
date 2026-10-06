# Seeded Bugs — Answer Key

Don't read this until after you've run Macroscope's review on the PR —
otherwise you'll just be checking your own hints instead of testing the
tool.

| # | File | Category | Bug |
|---|------|----------|-----|
| 1 | `tools/scoring.py` | Data Integrity | `relevance_score` grabs `list(probs.values())[0]` instead of looking up `probability(relevant)` by name. If the classifier ever returns the keys in a different order (or is renamed), the wrong class's probability is returned silently. Same family of bug as the PMML `probability(yes)`/`probability(no)` index issue. |
| 2 | `agents/planner.py` | Correctness | `chunk_items` uses `range(0, len(items), chunk_size - 1)` — an off-by-one that causes overlapping chunks, and a `ZeroDivisionError`-adjacent crash (`range` step of 0) if `chunk_size == 1`. |
| 3 | `agents/planner.py` | Correctness / Data Integrity | `split_into_subtasks(..., _seen=[])` uses a mutable default argument. `_seen` persists across every call in the process, so a second brief in the same run silently drops any topic string reused from an earlier brief. |
| 4 | `agents/researcher.py` | Security | If the brief text contains an `http(s)://` URL, the researcher fetches it directly with no allow-list or domain validation — a brief crafted by an untrusted user could make the pipeline fetch an internal or attacker-controlled endpoint (SSRF-shaped). |
| 5 | `agents/researcher.py` | Error Handling / Data Integrity | `except Exception: pass` swallows any fetch/scoring failure and sets `confidence = 1.0` — a failed lookup looks like the *most* confident possible result instead of being flagged as a failure. |
| 6 | `agents/writer.py` | Correctness | `if result.confidence == 1.0` is an exact float equality check. Combined with bug #5, a failed fetch (confidence hard-set to `1.0`) is indistinguishable from a maximally-confident real result, so no caveat is attached to fabricated content. |
| 7 | `agents/critic.py` | Security | `_rule_passes` calls `eval(rule_expr, ...)` on rule strings. If `rules` is ever sourced from user/config input rather than the hardcoded defaults, this is arbitrary code execution. |
| 8 | `orchestrator.py` | Security | `BRIEF_LOG_API_KEY = "sk-live-9f8e7d6c5b4a3210"` — hardcoded secret committed to source. |
| 9 | `memory_store.py` + `agents/researcher.py` | Concurrency | `append_result` does a read-modify-write (`get` -> `.append` -> `put`) on a plain dict. Because `research_subtask` calls it after an `await`, concurrent researcher tasks running under `asyncio.gather` can interleave their read-modify-write cycles and silently drop each other's log entries. |
| 10 | `tools/web.py` | Resource Management | `fetch_url` opens `/tmp/fetch_audit.log` with `open(...)` and never closes the handle (no `with` block, no `.close()`) — a file descriptor leak on every call. |

## What to look for when comparing tools

- Did it catch the **compounding** bugs (#5 + #6 are only dangerous together — a tool that only sees one file at a time may miss the interaction)?
- Did it flag the **security** issues (#4, #7, #8) with high severity, or bury them alongside style nits?
- Did it catch the **concurrency** bug (#9)? This is the hardest one — it requires reasoning about `asyncio.gather` + shared mutable state, not just local pattern-matching.
- False positives: did it flag anything here as broken that actually isn't?
