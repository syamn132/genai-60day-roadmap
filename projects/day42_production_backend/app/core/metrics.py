
from prometheus_client import (
    Counter,
    Histogram,
)


HTTP_REQUESTS = Counter(
    "day42_http_requests_total",
    "Total HTTP requests received",
    ["method", "route", "status"],
)


HTTP_DURATION = Histogram(
    "day42_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route"],
)


JOB_FINISHED = Counter(
    "day42_jobs_finished_total",
    "Background jobs reaching a final state",
    ["outcome"],
)
