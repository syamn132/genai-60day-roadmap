
from prometheus_client import (
    Counter,
    Histogram,
    CONTENT_TYPE_LATEST,
    generate_latest,
)

from fastapi.responses import Response


# ---------------------------------------
# METRIC 1 — HTTP REQUEST COUNT
# ---------------------------------------

HTTP_REQUESTS_TOTAL = Counter(
    "day41_http_requests_total",
    "Total HTTP requests handled by the API",
    ["method", "route", "status_code"],
)


# ---------------------------------------
# METRIC 2 — REQUEST LATENCY
# ---------------------------------------

HTTP_REQUEST_DURATION = Histogram(
    "day41_http_request_duration_seconds",
    "HTTP request processing duration",
    ["method", "route"],
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.0,
        5.0,
    ),
)


# ---------------------------------------
# METRICS ENDPOINT RESPONSE
# ---------------------------------------

def metrics_response():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
