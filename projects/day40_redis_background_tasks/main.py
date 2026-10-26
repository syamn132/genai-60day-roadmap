from uuid import uuid4

from fastapi import (
    BackgroundTasks,
    FastAPI,
    HTTPException,
    status,
)

from pydantic import BaseModel, Field

from tasks import (
    get_redis,
    save_job,
    load_job,
    process_report,
)


app = FastAPI(
    title="Day 40 — Redis & Background Tasks",
    version="1.0.0",
)


class ReportRequest(BaseModel):
    topic: str = Field(
        min_length=3,
        max_length=100,
    )


@app.get("/health")
def health():
    client = get_redis()

    try:
        redis_ok = client.ping()
    finally:
        client.close()

    return {
        "status": "ok",
        "redis_connected": redis_ok,
    }


@app.post(
    "/reports",
    status_code=status.HTTP_202_ACCEPTED,
)
def create_report(
    data: ReportRequest,
    background_tasks: BackgroundTasks,
):
    job_id = uuid4().hex

    save_job(
        job_id,
        topic=data.topic,
        status="queued",
        result="",
    )

    background_tasks.add_task(
        process_report,
        job_id,
        data.topic,
    )

    return {
        "message": "Report processing accepted",
        "job_id": job_id,
        "status": "queued",
    }


@app.get("/reports/{job_id}")
def get_report_status(job_id: str):
    job = load_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "job_id": job_id,
        **job,
    }