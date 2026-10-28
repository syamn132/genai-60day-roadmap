
import time
from uuid import uuid4

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Query,
)

from logging_config import configure_logging

from monitoring import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION,
    metrics_response,
)

from error_handling import (
    AppError,
    register_exception_handlers,
)


app = FastAPI(
    title="Day 41 — Logging & Monitoring",
    version="1.1.0",
)

logger = configure_logging()

register_exception_handlers(
    app,
    logger,
)


# ---------------------------------------
# PART 1 + PART 2
# LOGGING AND MONITORING MIDDLEWARE
# ---------------------------------------

@app.middleware("http")
async def log_and_monitor_requests(
    request: Request,
    call_next,
):

    # Do not count Prometheus scraping itself.
    if request.url.path == "/metrics":
        return await call_next(request)

    request_id = uuid4().hex[:12]

    request.state.request_id = request_id   # Make ID available to exception handlers.

    start_time = time.perf_counter()

    status_code = 500

    try:
        response = await call_next(request)

        status_code = response.status_code

        response.headers["X-Request-ID"] = request_id

        return response

    except Exception:
        logger.exception(
            "request_failed request_id=%s "
            "method=%s path=%s",
            request_id,
            request.method,
            request.url.path,
        )

        raise

    finally:
        duration_seconds = (
            time.perf_counter() - start_time
        )

        # Prefer the matched route template,
        # not the raw dynamic URL.
        route = request.scope.get("route")

        route_path = (
            route.path
            if route is not None
            else "unmatched"
        )

        # Increment request count.
        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            route=route_path,
            status_code=str(status_code),
        ).inc()

        # Record request duration.
        HTTP_REQUEST_DURATION.labels(
            method=request.method,
            route=route_path,
        ).observe(duration_seconds)

        # Retain our Part 1 logging.
        logger.info(
            "http_request request_id=%s "
            "method=%s path=%s "
            "status=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            status_code,
            duration_seconds * 1000,
        )


# ---------------------------------------
# EXISTING PART 1 ENDPOINTS
# ---------------------------------------

@app.get("/health")
def health():
    logger.debug("Health check endpoint executed")

    return {
        "status": "ok",
        "service": "day41-logging-monitoring",
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):

    if product_id != 1:

        logger.warning(
            "product_not_found product_id=%s",
            product_id,
        )

        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    logger.info(
        "product_retrieved product_id=%s",
        product_id,
    )

    return {
        "id": 1,
        "name": "Laptop",
        "price": 65000,
    }


@app.get("/logging-demo")
def logging_demo():

    logger.info("Demonstration endpoint called")
    logger.warning("Demonstration warning generated")
    logger.error("Simulated error event for learning")

    return {
        "message": "Log events generated",
        "status": "demo_completed",
    }


# ---------------------------------------
# PART 2 — MONITORING ENDPOINT
# ---------------------------------------

@app.get("/metrics", include_in_schema=False)
def metrics():
    return metrics_response()


# ---------------------------------------
# PART 2 — SIMULATE LATENCY
# ---------------------------------------

@app.get("/slow")
def simulate_slow_request(
    delay_ms: int = Query(
        default=250,
        ge=0,
        le=1000,
    ),
):

    logger.info(
        "simulated_slow_request delay_ms=%s",
        delay_ms,
    )

    time.sleep(delay_ms / 1000)

    return {
        "message": "Slow request simulation complete",
        "delay_ms": delay_ms,
    }


@app.get("/divide")
def divide(
    a: float,
    b: float,
):

    if b == 0:
        raise AppError(
            status_code=400,
            code="DIVISION_BY_ZERO",
            message="Parameter b must not be zero",
        )

    return {
        "a": a,
        "b": b,
        "result": a / b,
    }