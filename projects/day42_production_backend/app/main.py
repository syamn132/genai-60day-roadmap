
import logging
import time

from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.jobs import router as jobs_router

from app.core.logging_config import configure_logging
from app.core.error_handlers import install_error_handlers
from app.core.metrics import (
    HTTP_REQUESTS,
    HTTP_DURATION,
)


configure_logging()

logger = logging.getLogger("day42.http")


app = FastAPI(
    title="Day 42 — Production Backend",
    description="Sprint 4 Backend Engineering Project",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(jobs_router)


install_error_handlers(app)


@app.middleware("http")
async def observe_requests(
    request: Request,
    call_next,
):

    request_id = uuid4().hex

    request.state.request_id = request_id

    started = time.perf_counter()

    try:

        response = await call_next(request)

    except Exception:

        logger.exception(
            "Unhandled HTTP request error",
            extra={"request_id": request_id},
        )

        response = JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id,
            },
        )

    duration_seconds = time.perf_counter() - started

    route = getattr(
        request.scope.get("route"),
        "path",
        "unmatched",
    )

    if route != "/metrics":

        HTTP_REQUESTS.labels(
            method=request.method,
            route=route,
            status=str(response.status_code),
        ).inc()

        HTTP_DURATION.labels(
            method=request.method,
            route=route,
        ).observe(duration_seconds)

    logger.info(
        "HTTP request completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "route": route,
            "status_code": response.status_code,
            "duration_ms": round(
                duration_seconds * 1000,
                2,
            ),
        },
    )

    response.headers["X-Request-ID"] = request_id

    return response


@app.get("/metrics", include_in_schema=False)
def metrics():

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/")
def root():

    return {
        "message": "Day 42 Production Backend API",
        "version": "0.1.0",
    }
