
import json
import logging
import os

import redis

from redis.exceptions import RedisError


logger = logging.getLogger("day42.redis")


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://127.0.0.1:6379/0",
)

CACHE_TTL_SECONDS = 60


redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)


def job_status_key(job_id: int) -> str:

    return f"day42:job:{job_id}:status"


def cache_job_status(
    job_id: int,
    status: str,
    result: str | None,
) -> None:

    value = json.dumps(
        {
            "status": status,
            "result": result,
        }
    )

    try:
        redis_client.set(
            job_status_key(job_id),
            value,
            ex=CACHE_TTL_SECONDS,
        )

        logger.info(
            "Redis cache SET for job %s",
            job_id,
        )

    except RedisError as exc:

        logger.warning(
            "Redis cache write unavailable for job %s: %s",
            job_id,
            type(exc).__name__,
        )


def get_cached_job_status(
    job_id: int,
) -> dict[str, str | None] | None:

    try:
        value = redis_client.get(
            job_status_key(job_id)
        )

    except RedisError as exc:

        logger.warning(
            "Redis cache read unavailable for job %s: %s",
            job_id,
            type(exc).__name__,
        )

        return None

    if value is None:

        logger.info(
            "Redis cache MISS for job %s",
            job_id,
        )

        return None

    try:
        data = json.loads(value)

    except (ValueError, TypeError):

        logger.warning(
            "Invalid Redis JSON for job %s",
            job_id,
        )

        return None

    if not isinstance(data, dict):
        return None

    cached_status = data.get("status")

    if (
        not isinstance(cached_status, str)
        or cached_status not in {
            "pending",
            "running",
            "completed",
            "failed",
        }
    ):
        return None

    result = data.get("result")

    if result is not None and not isinstance(result, str):
        return None

    logger.info(
        "Redis cache HIT for job %s",
        job_id,
    )

    return {
        "status": data["status"],
        "result": result,
    }
