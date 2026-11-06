
import logging
import time

from app.db.models import Job
from app.db.session import SessionLocal

from app.services.job_cache import cache_job_status

from app.core.metrics import JOB_FINISHED


logger = logging.getLogger("day42.worker")


def simulate_ai_response(topic: str) -> str:

    time.sleep(4)

    if topic.strip().lower() == "simulate_failure":
        raise RuntimeError("Intentional demo failure")

    return (
        f"Simulated AI response for: {topic}. "
        "Retrieval-Augmented Generation (RAG) "
        "retrieves relevant information before "
        "an LLM generates its answer."
    )


def process_job(job_id: int) -> None:

    logger.info("Starting background job %s", job_id)

    try:

        # STEP 1: Mark the job as running.
        with SessionLocal() as session:

            job = session.get(Job, job_id)

            if job is None:
                logger.warning(
                    "Job %s does not exist",
                    job_id,
                )
                return

            if job.status != "pending":
                logger.warning(
                    "Job %s is not pending",
                    job_id,
                )
                return

            topic = job.topic
            job.status = "running"

            session.commit()

        # NEW: Cache the running state.
        cache_job_status(job_id, "running", None)

        # STEP 2: Simulate AI processing.
        result = simulate_ai_response(topic)

        # STEP 3: Save the completed result.
        with SessionLocal() as session:

            job = session.get(Job, job_id)

            if job is None:
                logger.warning(
                    "Job %s disappeared",
                    job_id,
                )
                return

            if job.status != "running":
                logger.warning(
                    "Job %s changed state",
                    job_id,
                )
                return

            job.result = result
            job.status = "completed"

            session.commit()

        # NEW: Cache the completed state.
        cache_job_status(job_id, "completed", result)

        JOB_FINISHED.labels(
            outcome="completed",
        ).inc()

        logger.info(
            "Background job %s completed",
            job_id,
        )

    except Exception:

        logger.exception(
            "Background job %s failed",
            job_id,
        )

        try:
            with SessionLocal() as session:

                job = session.get(Job, job_id)

                if job is not None:

                    job.status = "failed"
                    job.result = None

                    session.commit()

                    # NEW: Cache the failure state.
                    cache_job_status(
                        job_id,
                        "failed",
                        None,
                    )

                    JOB_FINISHED.labels(
                        outcome="failed",
                    ).inc()

        except Exception:
            logger.exception(
                "Could not save failure for job %s",
                job_id,
            )
