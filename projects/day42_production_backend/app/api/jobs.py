
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_user

from app.db.models import Job, User
from app.db.session import get_session

from app.schemas.job import (
    JobCreate,
    JobPublic,
    JobStatusPublic,
)

from app.services.job_worker import process_job

from app.services.job_cache import (
    cache_job_status,
    get_cached_job_status,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


# ----------------------------------
# CREATE JOB
# ----------------------------------

@router.post(
    "",
    response_model=JobPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    data: JobCreate,
    background_tasks: BackgroundTasks,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    session: Annotated[
        Session,
        Depends(get_session),
    ],
):

    # Create a new pending job.
    job = Job(
        user_id=current_user.id,
        topic=data.topic,
        status="pending",
    )

    # Save it permanently first.
    session.add(job)
    session.commit()
    session.refresh(job)

    # NEW: Save the initial pending state in Redis.
    cache_job_status(
        job.id,
        job.status,
        job.result,
    )

    # Schedule processing after the response.
    background_tasks.add_task(
        process_job,
        job.id,
    )

    # Return the newly created job.
    return job


# ----------------------------------
# LIST MY JOBS
# ----------------------------------

@router.get(
    "",
    response_model=list[JobPublic],
)
def list_my_jobs(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    session: Annotated[
        Session,
        Depends(get_session),
    ],
):

    statement = (
        select(Job)
        .where(Job.user_id == current_user.id)
        .order_by(Job.id.desc())
    )

    jobs = session.scalars(statement).all()

    return jobs


# ----------------------------------
# GET A SPECIFIC JOB
# ----------------------------------

@router.get(
    "/{job_id}",
    response_model=JobPublic,
)
def get_job(
    job_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    session: Annotated[
        Session,
        Depends(get_session),
    ],
):

    job = session.scalar(
        select(Job).where(
            Job.id == job_id,
            Job.user_id == current_user.id,
        )
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job

# ----------------------------------
# GET JOB STATUS
# ----------------------------------

@router.get(
    "/{job_id}/status",
    response_model=JobStatusPublic,
)
def get_job_status(
    job_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    session: Annotated[
        Session,
        Depends(get_session),
    ],
):

    # 1. Verify ownership using PostgreSQL.
    owner_id = session.scalar(
        select(Job.user_id).where(
            Job.id == job_id
        )
    )

    if owner_id is None or owner_id != current_user.id:

        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    # 2. Check the Redis cache.
    cached = get_cached_job_status(job_id)

    if cached is not None:

        return JobStatusPublic(
            job_id=job_id,
            status=cached["status"],
            result=cached["result"],
            source="redis",
        )

    # 3. Cache miss: load from PostgreSQL.
    job = session.get(Job, job_id)

    if job is None:

        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    # 4. Refill the cache for final states.
    if job.status in ("completed", "failed"):

        cache_job_status(
            job.id,
            job.status,
            job.result,
        )

    # 5. Return the database result.
    return JobStatusPublic(
        job_id=job.id,
        status=job.status,
        result=job.result,
        source="postgresql",
    )
