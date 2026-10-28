from datetime import datetime, timezone
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)


class AppError(Exception):
    """
    Controlled application/business error.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ):
        super().__init__(message)

        self.status_code = status_code
        self.code = code
        self.message = message


def error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details=None,
    headers=None,
):
    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    error_data = {
        "code": code,
        "message": message, 
        "request_id": request_id,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    if details is not None:
        error_data["details"] = details

    response_headers = dict(headers or {})

    if request_id:
        response_headers["X-Request-ID"] = request_id

    return JSONResponse(
        status_code=status_code,
        content={"error": error_data},
        headers=response_headers,
    )


def register_exception_handlers(
    app: FastAPI,
    logger: logging.Logger,
):

    # ----------------------------------
    # 1. CUSTOM APPLICATION ERRORS
    # ----------------------------------

    @app.exception_handler(AppError)
    async def app_error_handler(
        request: Request,
        exc: AppError,
    ):
        logger.warning(
            "application_error code=%s path=%s",
            exc.code,
            request.url.path,
        )

        return error_response(
            request=request,
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
        )

    # ----------------------------------
    # 2. HTTP ERRORS
    # ----------------------------------

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        message = (
            exc.detail
            if isinstance(exc.detail, str)
            and exc.status_code < 500
            else "HTTP request failed"
        )

        return error_response(
            request=request,
            status_code=exc.status_code,
            code=f"HTTP_{exc.status_code}",
            message=message,
            headers=exc.headers,
        )

    # ----------------------------------
    # 3. PYDANTIC VALIDATION ERRORS
    # ----------------------------------

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        safe_details = [
            {
                "field": ".".join(
                    str(part)
                    for part in error["loc"]
                ),
                "type": error["type"],
            }
            for error in exc.errors()
        ]

        logger.warning(
            "validation_failed path=%s",
            request.url.path,
        )

        return error_response(
            request=request,
            status_code=422,
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=safe_details,
        )

    # ----------------------------------
    # 4. UNEXPECTED SERVER ERRORS
    # ----------------------------------

    @app.exception_handler(Exception)
    async def unexpected_error_handler(
        request: Request,
        exc: Exception,
    ):
        # The existing request middleware
        # already logs the full traceback.
        # Never expose exception details
        # to the HTTP client.

        return error_response(
            request=request,
            status_code=500,
            code="INTERNAL_SERVER_ERROR",
            message="An internal error occurred",
        )
