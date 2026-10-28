#!/usr/bin/env python3
"""Update the verified Day 40 SSOT markdown through completed Day 41.

Usage:
    python update_roadmap.py
    python update_roadmap.py --source "/path/to/Pasted markdown_day40.md"

The input is never modified. The script refuses to overwrite its output,
requires the precise expected Day 40 version, and checks retention of prior days.
"""

from argparse import ArgumentParser
from datetime import date
from pathlib import Path

DEFAULT_CANDIDATES = [
    "Pasted markdown_day40.md",
    "GenAI_60_Day_Roadmap_Updated_Day40.md",
]
DEFAULT_OUTPUT = "GenAI_60_Day_Roadmap_Updated_Day41.md"

DAY41_RECORD = """**Day 41 status:** ✅ Completed — Logging (Part 1), Monitoring (Part 2), and Error Handling (Part 3).

**Day 41 project:** `projects/day41_logging_monitoring_error_handling/`

**Day 41 Part 1 status:** ✅ Completed — Python logging and FastAPI request logging.

**Day 41 Part 1 concepts and implementation:**

- Python `logging` versus ad-hoc `print()`; DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Named application logger, severity thresholds, formatters, and console/file handlers.
- `RotatingFileHandler` writing to `logs/app.log` with a bounded file size and backup retention.
- `logger.error()` versus `logger.exception()` with traceback.
- FastAPI HTTP middleware for request correlation IDs, HTTP methods/paths/statuses and elapsed milliseconds.
- Avoid logging secrets, credentials, tokens and sensitive request data.
- Repository `.gitignore` uses `*.log` and a Day 41 log-directory exclusion.

**Day 41 Part 1 practical verification:**

- `logging_demo.py` exercised normal log severities and captured a deliberate `ZeroDivisionError` traceback.
- Saved `logs/app.log` showed DEBUG events, request timing, statuses and request IDs.
- `GET /health` → HTTP 200.
- `GET /products/1` → HTTP 200.
- `GET /products/99` → HTTP 404 with a warning log.
- `GET /logging-demo` → HTTP 200 with INFO, WARNING and simulated ERROR events.
- Terminal and file logs showed request IDs and millisecond request durations.

**Day 41 Part 2 status:** ✅ Completed — Prometheus-style monitoring instrumentation. The five practical checkpoints were user-confirmed.

**Day 41 Part 2 concepts and implementation:**

- Difference between logs, metrics and traces; four signals: latency, traffic, errors and saturation.
- Prometheus `/metrics` HTTP exposition via the Python `prometheus-client`.
- Request Counter: `day41_http_requests_total` with method, route template and status-code labels.
- Latency Histogram: `day41_http_request_duration_seconds` with bucket, sum and count measurements.
- Existing middleware extended with `.inc()` and `.observe(duration_seconds)` in `finally`.
- Dynamic route templates used instead of per-user or per-resource IDs to limit label cardinality.
- `/slow?delay_ms=500` introduced a controlled latency test.
- Local process metrics reset on restart; multi-worker and production security limitations discussed.

**Day 41 Part 2 practical verification:**

- Monitoring dependencies installed; previous logging endpoints kept working.
- `/metrics` exposed HTTP request counters and latency histograms.
- Additional `/health` calls increased the request count.
- `/slow?delay_ms=500` produced a latency observation.
- Part 2's original five checks were reported successful by the user.
- Later direct terminal inspection confirmed counters for actual HTTP 200, 400, 404, 409, 422 and 500 requests.

**Day 41 Part 3 status:** ✅ Completed — Custom FastAPI exception handling, safe errors and integrated observability.

**Day 41 Part 3 concepts and implementation:**

- Controlled application errors versus unexpected failures.
- HTTP status semantics: 200, 400, 401, 403, 404, 409, 422, 429, 500 and 503.
- Reusable `AppError` for application/business conditions.
- Specialized handlers for `StarletteHTTPException`, `RequestValidationError`, and unexpected `Exception`.
- Standardized JSON error envelope: code, safe message, request_id, timestamp, and safe validation metadata when relevant.
- Request ID attached to `request.state` and reused in response header/body and application logs.
- Validation details limited to parameter locations and error types; no raw input/secrets exposed.
- Unexpected 500 response sanitized while the real traceback was preserved in logs.
- Logging and Prometheus counter/histogram recording integrated with error responses.
- Deliberate `/unhandled-demo` route used for a local-only exception test, not deployment.

**Day 41 Part 3 directly verified practical results (2026-10-27):**

```text
GET /divide?a=10&b=2     → HTTP 200, result=5.0
GET /divide?a=10&b=0     → HTTP 400, code=DIVISION_BY_ZERO
GET /conflict-demo       → HTTP 409, code=RESOURCE_CONFLICT
GET /products/abc        → HTTP 422, code=VALIDATION_ERROR, field=path.product_id, type=int_parsing
GET /products/99         → HTTP 404, code=HTTP_404
GET /unhandled-demo      → HTTP 500, code=INTERNAL_SERVER_ERROR
```

- HTTP error responses included safe messages, `X-Request-ID` header, matching JSON request IDs and timestamps.
- The unexpected error response did not expose the internal Python `RuntimeError`; the server log contained a full traceback and `request_failed` event.
- The `Exception in ASGI application` traceback was expected for the deliberately unhandled local test.
- `tail -n 40 logs/app.log` worked after changing into the Day 41 project folder; the initial attempt from repository root failed only due to relative path.
- Prometheus request-counter output contained real status-code series for 200, 400, 404, 409, 422 and 500.
- `route="unmatched"` appeared for non-application/missing routes; not a failure.

**Day 41 project files and responsibilities:**

- `logging_config.py` — logger configuration, console/file handlers, formatter, file rotation.
- `logging_demo.py` — log-severity and exception-traceback exercise.
- `monitoring.py` — Prometheus Counter, Histogram and metrics-response helper.
- `error_handling.py` — custom exception types, standardized error responses and handlers.
- `main.py` — FastAPI routes, combined logging/monitoring middleware and error demos.
- `requirements.txt` — `fastapi[standard]`, `prometheus-client`.
- `README.md` — project documentation.
- `logs/app.log` — generated local application logs, excluded from Git.

**Day 41 one-pagers:** ✅ Completed — four separate infographic PNGs:
- `Day41_Part1_Logging_OnePager.png`
- `Day41_Part2_Monitoring_OnePager.png`
- `Day41_Part3_Error_Handling_OnePager.png`
- `Day41_Master_OnePager.png`

**Day 41 learning outcome:** Implemented and verified FastAPI application logging, request IDs, rotating file logs, Prometheus counters and histograms, middleware instrumentation, business/validation exception handlers, and safe correlated API error responses.

**Day 42 roadmap:**

- Sprint 4 project: Production Backend — NEXT.
- Integrate FastAPI, PostgreSQL, SQLAlchemy, authentication, Redis caching, background processing, logging, monitoring and error handling.
"""


def replace_exact(content: str, old: str, new: str) -> str:
    count = content.count(old)
    if count != 1:
        raise ValueError(f"Expected exactly 1 occurrence, found {count}: {old[:100]!r}")
    return content.replace(old, new, 1)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Day 40 roadmap markdown")
    parser.add_argument("--output", type=Path, help="New Day 41 markdown path")
    args = parser.parse_args()

    if args.source is not None:
        source = args.source
    else:
        source = next((Path(name) for name in DEFAULT_CANDIDATES
                       if Path(name).is_file()), None)
        if source is None:
            raise FileNotFoundError(
                f"Put the Day 40 markdown beside this script: "
                f"{', '.join(DEFAULT_CANDIDATES)}"
            )
    output = args.output or source.parent / DEFAULT_OUTPUT
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError("Input and output paths must differ.")
    if output.exists():
        raise FileExistsError(f"Output already exists, refusing to overwrite: {output}")

    original = source.read_text(encoding="utf-8")
    updated = original

    replacements = {
        "**Last updated:** 2026-10-26":
            "**Last updated:** 2026-10-27",
        "**Overall progress:** Days 1–40 completed (66.7%). 20 days remaining.":
            "**Overall progress:** Days 1–41 completed (68.3%). 19 days remaining.",
        "**Next exact step:** Day 41 — Part 1 Logging; Part 2 Monitoring; Part 3 Error Handling.":
            "**Next exact step:** Day 42 — Sprint 4 Project: Production Backend.",
        "⬜ Day 41":
            "✅ Day 41",
    }
    for old, new in replacements.items():
        updated = replace_exact(updated, old, new)

    placeholder = (
        "**Day 41 roadmap:**\n\n"
        "- Part 1: Logging — NEXT.\n"
        "- Part 2: Monitoring — Pending.\n"
        "- Part 3: Error Handling — Pending."
    )
    updated = replace_exact(updated, placeholder, DAY41_RECORD.strip())

    must_keep = [
        "**Day 39 status:** ✅ Completed",
        "**Day 40 status:** ✅ Completed",
        "Day 40 Part 1 directly verified practical results",
        "Day 40 Part 2 directly verified practical results",
        "🟠 Sprint 4 — Backend Engineering",
        "⬜ Day 42",
        "⬜ Day 60",
        "**Day 16 project status:**",
    ]
    for text in must_keep:
        if text not in updated:
            raise AssertionError(f"Prior roadmap marker missing: {text}")

    expected = [
        "**Day 41 status:** ✅ Completed",
        "**Day 41 Part 1 status:** ✅ Completed",
        "**Day 41 Part 2 status:** ✅ Completed",
        "**Day 41 Part 3 status:** ✅ Completed",
        "**Day 41 one-pagers:** ✅ Completed",
        "**Day 42 roadmap:**",
        "Days 1–41 completed (68.3%)",
        "✅ Day 41",
    ]
    for text in expected:
        if text not in updated:
            raise AssertionError(f"Update not present: {text}")

    if updated.count("**Day 41 status:**") != 1:
        raise AssertionError("Duplicate Day 41 completion records")
    if updated.count("✅ Day 41") != 1:
        raise AssertionError("Duplicate Day 41 checklist entry")

    # Before writing, verify all changes are exactly the intended five edits.
    reverted = updated
    reverted = replace_exact(reverted, DAY41_RECORD.strip(), placeholder)
    for old, new in replacements.items():
        reverted = replace_exact(reverted, new, old)
    if reverted != original:
        raise AssertionError("Unexpected changes to prior Markdown content.")

    output.write_text(updated, encoding="utf-8")
    print("=" * 60)
    print("DAY 41 ROADMAP UPDATE SUCCESSFUL")
    print("=" * 60)
    print(f"Source retained: {source.resolve()}")
    print(f"Output created: {output.resolve()}")
    print(f"Original lines: {len(original.splitlines())}")
    print(f"Updated lines: {len(updated.splitlines())}")
    print(f"Output bytes: {output.stat().st_size:,}")
    print("Progress: 41/60 days (68.3%), 19 days remaining")
    print("Day 41: Logging, Monitoring, Error Handling — complete")
    print("Next: Day 42 — Production Backend Project")
    print("=" * 60)


if __name__ == "__main__":
    main()
