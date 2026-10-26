"""Update the GenAI roadmap from Day 39 to Day 40 without losing earlier content.

Run this script from the directory containing your Day 39 Markdown file:
    python update_roadmap.py

Or choose the source explicitly:
    python update_roadmap.py --source "Pasted markdown_day39.md"

The script creates GenAI_60_Day_Roadmap_Updated_Day40.md; it never overwrites
its source or an existing output file, and it refuses unexpected input versions.
"""

from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_SOURCES = (
    "Pasted markdown_day39.md",
    "GenAI_60_Day_Roadmap_Updated_Day39.md",
    "Pasted markdown.md",
)
DEFAULT_OUTPUT = "GenAI_60_Day_Roadmap_Updated_Day40.md"


DAY40_RECORD = """**Day 40 status:** ✅ Completed — Redis (Part 1) and Background Tasks (Part 2).

**Day 40 project:** `projects/day40_redis_background_tasks/`

**Day 40 Part 1 status:** ✅ Completed — Redis, including verified local server and Python cache-aside practicals.

**Day 40 Part 1 concepts and implementation:**

- Redis as an in-memory data store; how it complements PostgreSQL as the primary database.
- Keys, values, strings, TTL/expiration, cache hits, cache misses, and cache invalidation.
- Redis CLI operations: `PING`, `SET`, `GET`, `TTL`, and `DEL`.
- Redis Python client (`redis-py`) and `decode_responses=True`.
- Cache-aside pattern: check Redis → on miss read source data → cache with TTL → return response.
- Cache invalidation after a source-data update, plus awareness of stale values.
- Redis use cases in backend/GenAI systems: caching, rate limits, temporary state, and job-status storage.

**Day 40 Redis installation and troubleshooting:**

- Environment: Intel Mac running macOS Sequoia 15.7.8.
- Homebrew Redis installation attempted to build many dependencies from source and failed at GMP `autoreconf`; Redis was not installed through Homebrew.
- Installed MacPorts 2.12.7 and Redis 8.8.0_0 successfully using `sudo port install redis`.
- Started the managed service using `sudo port load redis`.
- Verified `/opt/local/bin/redis-cli ping` returned `PONG`.
- Installed Python `redis` client 8.1.0 in the existing `.venv`.

**Day 40 Part 1 directly verified practical results:**

```text
redis-cli ping                          → PONG
SET day40:test "Hello Redis" EX 120     → OK
GET day40:test                          → "Hello Redis"
TTL day40:test                          → 120 seconds in the captured run
DEL day40:test                          → (integer) 1

python redis_demo.py:
  PING True; SET and GET succeeded; TTL=120; DEL=1; deleted value=None.

python cache_aside_demo.py:
  First request: CACHE MISS → simulated database read → cache write (60s).
  Second request: CACHE HIT → cached product returned.
  Updated product stock: 10 → 15.
  After invalidation: CACHE MISS → refreshed stock=15.
  Final output: CACHE-ASIDE TEST COMPLETED.
```

**Day 40 Part 2 status:** ✅ Completed — FastAPI Background Tasks with Redis job-status tracking.

**Day 40 Part 2 concepts and implementation:**

- FastAPI `BackgroundTasks` and registering synchronous tasks using `background_tasks.add_task()`.
- HTTP 202 Accepted: request accepted for processing; not a guarantee of task completion.
- In-process task execution after the response, using Starlette/FastAPI execution facilities.
- Simulated report generation with `time.sleep(6)`; background start/completion logs.
- Unique job IDs generated with `uuid4().hex`.
- Redis hash status tracking: `queued` → `running` → `completed` (or `failed`).
- Redis hash operations and one-hour job-status TTL.
- API endpoints: `GET /health`, `POST /reports`, `GET /reports/{job_id}`.
- Missing job handling with HTTP 404.
- Production limitation: `BackgroundTasks` runs in the API process; Redis storing status does **not** create a durable task queue. Dedicated queues/workers (such as Celery or RQ) are appropriate for heavier or restart-safe workloads.

**Day 40 Part 2 directly verified practical results:**

- `GET /health` → HTTP 200, Redis connection working.
- `POST /reports` with topic `RAG Architecture` → HTTP 202 Accepted.
- Terminal trace: `BACKGROUND STARTED` followed by `BACKGROUND COMPLETED` for the same job ID.
- `GET /reports/{job_id}` for the real job → HTTP 200.
- Corrected Swagger test: `GET /reports/not-a-real-job` → HTTP 404 with `{"detail": "Job not found"}`.
- An initial Swagger attempt included `GET /reports/` inside the `job_id` parameter, yielding a routing-level 404; correcting the parameter verified the application's own 404 handling.
- The full successful job-status JSON body was not separately pasted; task completion is supported by server logs and the user-confirmed practicals.

**Day 40 project files and responsibilities:**

- `redis_demo.py` — basic Redis connection, SET/GET/TTL/DEL demonstration.
- `cache_aside_demo.py` — cache miss/hit/invalidation with a simulated Python-dictionary database.
- `tasks.py` — background report processing and Redis job-status helpers.
- `main.py` — FastAPI health, report-submission, and job-status endpoints.
- `requirements.txt` — `fastapi[standard]` and `redis`.
- `README.md` — documentation file created for the Day 40 project.

**Day 40 one-pagers:** ✅ Completed — three separate revision images: Part 1 Redis, Part 2 Background Tasks, and Day 40 Master one-pager.

**Day 40 learning outcome:** Implemented Redis key-value operations and a cache-aside example, then integrated FastAPI BackgroundTasks with Redis-based job-status lookup. Verified HTTP 200/202/404, the background execution trace, and cache invalidation behavior.

**Day 41 roadmap:**

- Part 1: Logging — NEXT.
- Part 2: Monitoring — Pending.
- Part 3: Error Handling — Pending."""


REPLACEMENTS = (
    (
        "**Last updated:** 2026-10-23",
        "**Last updated:** 2026-10-26",
    ),
    (
        "**Overall progress:** Days 1–39 completed (65.0%). 21 days remaining.",
        "**Overall progress:** Days 1–40 completed (66.7%). 20 days remaining.",
    ),
    (
        "**Next exact step:** Day 40 — Part 1 Redis; Part 2 Background Tasks.",
        "**Next exact step:** Day 41 — Part 1 Logging; Part 2 Monitoring; Part 3 Error Handling.",
    ),
    (
        "⬜ Day 40",
        "✅ Day 40",
    ),
    (
        "**Day 40 roadmap:**\n\n- Part 1: Redis — NEXT.\n- Part 2: Background Tasks — Pending.",
        DAY40_RECORD,
    ),
)


def replace_once(content: str, old: str, new: str) -> str:
    count = content.count(old)
    if count != 1:
        raise ValueError(
            f"Expected exactly one occurrence, found {count}: {old[:100]!r}. "
            "Use the unmodified Day 39 Markdown as input."
        )
    return content.replace(old, new, 1)


def find_source(source_argument: Path | None) -> Path:
    if source_argument is not None:
        if not source_argument.is_file():
            raise FileNotFoundError(f"Day 39 Markdown not found: {source_argument}")
        return source_argument

    for filename in DEFAULT_SOURCES:
        candidate = Path(filename)
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "Place the Day 39 Markdown beside this script or provide --source FILE. "
        f"Tried: {', '.join(DEFAULT_SOURCES)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safely advance the complete GenAI Markdown roadmap to Day 40."
    )
    parser.add_argument("--source", type=Path, default=None,
                        help="Source Day 39 Markdown file")
    parser.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT),
                        help="New output Markdown file")
    args = parser.parse_args()

    source = find_source(args.source)
    output: Path = args.output

    if source.resolve() == output.resolve():
        raise ValueError("Source and output must be different files.")
    if output.exists():
        raise FileExistsError(
            f"{output} already exists. Refusing to overwrite it. "
            "Choose a different --output or move the existing file."
        )

    before = source.read_text(encoding="utf-8")
    if "**Day 39 status:** ✅ Completed" not in before:
        raise ValueError("Source does not contain a completed Day 39 record.")
    if "**Day 40 status:** ✅ Completed" in before:
        raise ValueError("Day 40 is already recorded as completed.")
    if "✅ Day 39" not in before or "⬜ Day 41" not in before:
        raise ValueError("Unexpected roadmap checklist status in source.")

    after = before
    for old, new in REPLACEMENTS:
        after = replace_once(after, old, new)

    # Explicit verification: previous days remain present, and no other changes
    # were made outside the five intentional replacements.
    for marker in (
        "**Day 25 status:**", "**Day 34 status:**", "**Day 35 status:**",
        "**Day 36 status:**", "**Day 37 status:**", "**Day 38 status:**",
        "**Day 39 status:** ✅ Completed", "**Day 40 status:** ✅ Completed",
        "**Day 40 Part 1 status:** ✅ Completed",
        "**Day 40 Part 2 status:** ✅ Completed",
        "**Day 40 one-pagers:** ✅ Completed",
        "**Day 41 roadmap:**", "✅ Day 40", "⬜ Day 41",
        "**Overall progress:** Days 1–40 completed (66.7%). 20 days remaining.",
    ):
        if marker not in after:
            raise AssertionError(f"Post-update verification failed: {marker}")

    reverse = after
    for old, new in reversed(REPLACEMENTS):
        reverse = replace_once(reverse, new, old)
    if reverse != before:
        raise AssertionError("Integrity check failed: unintended content changed.")

    output.parent.mkdir(parents=True, exist_ok=True)
    # 'x' mode prevents accidental overwrite, including at write time.
    with output.open("x", encoding="utf-8", newline="") as f:
        f.write(after)

    print("=" * 57)
    print("DAY 40 ROADMAP UPDATE SUCCESSFUL")
    print("=" * 57)
    print(f"Source (unchanged): {source.resolve()}")
    print(f"New output:         {output.resolve()}")
    print(f"Original lines:     {len(before.splitlines())}")
    print(f"Updated lines:      {len(after.splitlines())}")
    print("Progress:           40/60 days (66.7%) — 20 remaining")
    print("Part 1:             Redis — completed")
    print("Part 2:             Background Tasks — completed")
    print("One-pagers:         3 completed")
    print("Next:               Day 41 Logging / Monitoring / Error Handling")
    print("Integrity:          Prior content preserved; no original overwritten")
    print("=" * 57)


if __name__ == "__main__":
    main()
