
import time
import logging

import redis


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("day40")


def get_redis():
    return redis.Redis(
        host="127.0.0.1",
        port=6379,
        db=0,
        decode_responses=True,
    )


def save_job(job_id: str, **fields):
    client = get_redis()

    try:
        key = f"day40:job:{job_id}"

        client.hset(
            key,
            mapping={
                name: str(value)
                for name, value in fields.items()
            },
        )

        # Keep demo job data for one hour.
        client.expire(key, 3600)

    finally:
        client.close()


def load_job(job_id: str):
    client = get_redis()

    try:
        return client.hgetall(
            f"day40:job:{job_id}"
        )

    finally:
        client.close()


def process_report(job_id: str, topic: str):
    try:
        save_job(
            job_id,
            status="running",
        )

        logger.info(
            "BACKGROUND STARTED: job=%s topic=%s",
            job_id,
            topic,
        )

        # Simulate slow report processing.
        time.sleep(6)

        result = (
            f"Demo report completed for: {topic}"
        )

        save_job(
            job_id,
            status="completed",
            result=result,
        )

        logger.info(
            "BACKGROUND COMPLETED: job=%s",
            job_id,
        )

    except Exception:
        logger.exception(
            "BACKGROUND FAILED: job=%s",
            job_id,
        )

        try:
            save_job(
                job_id,
                status="failed",
                result="Background processing failed",
            )

        except Exception:
            logger.exception(
                "Unable to record failed job status"
            )
