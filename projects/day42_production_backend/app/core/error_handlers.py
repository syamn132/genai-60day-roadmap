
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from sqlalchemy.exc import OperationalError

from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)


logger = logging.getLogger("day42.errors")


def install_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(
        request: Request,
        exc: StarletteHTTPException,
    ):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "request_id": request.state.request_id,
            },
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ):

        safe_errors = [
            {
                "loc": list(error["loc"]),
                "msg": error["msg"],
                "type": error["type"],
            }
            for error in exc.errors()
        ]

        return JSONResponse(
            status_code=422,
            content={
                "detail": safe_errors,
                "request_id": request.state.request_id,
            },
        )

    @app.exception_handler(OperationalError)
    async def handle_database_error(
        request: Request,
        exc: OperationalError,
    ):

        logger.error(
            "Database operation failed",
            extra={
                "request_id": request.state.request_id,
            },
            exc_info=(
                type(exc),
                exc,
                exc.__traceback__,
            ),
        )

        return JSONResponse(
            status_code=503,
            content={
                "detail": "Database temporarily unavailable",
                "request_id": request.state.request_id,
            },
        )
