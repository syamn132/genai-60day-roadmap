
import json
import logging
import sys

from datetime import datetime, timezone


class JSONLogFormatter(logging.Formatter):

    def format(self, record):

        log_entry = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        fields = (
            "request_id",
            "method",
            "route",
            "status_code",
            "duration_ms",
            "job_id",
        )

        for field in fields:

            value = getattr(record, field, None)

            if value is not None:
                log_entry[field] = value

        if record.exc_info:
            log_entry["exception"] = (
                self.formatException(record.exc_info)
            )

        return json.dumps(
            log_entry,
            default=str,
        )


def configure_logging() -> None:

    app_logger = logging.getLogger("day42")

    if not app_logger.handlers:

        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(
            JSONLogFormatter()
        )

        app_logger.addHandler(handler)

    app_logger.setLevel(logging.INFO)

    app_logger.propagate = False
