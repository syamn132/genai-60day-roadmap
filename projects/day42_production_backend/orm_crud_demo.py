
import secrets
from uuid import uuid4

from pwdlib import PasswordHash
from sqlalchemy import select

from app.db.models import User, Job
from app.db.session import SessionLocal


password_hasher = PasswordHash.recommended()


def main():

    print("=" * 55)
    print("DAY 42 — SQLALCHEMY SESSIONS & CRUD")
    print("=" * 55)

    # Give every demo run a unique username.
    username = f"day42_demo_{uuid4().hex[:10]}"

    # Generate and hash a random demo password.
    random_password = secrets.token_urlsafe(32)
    hashed_password = password_hasher.hash(
        random_password
    )

    # -----------------------------------
    # CREATE
    # -----------------------------------

    print("\n1. CREATE USER AND JOB")

    with SessionLocal() as session:

        user = User(
            username=username,
            password_hash=hashed_password,
        )

        session.add(user)
        session.flush()

        user_id = user.id

        job = Job(
            user_id=user_id,
            topic="Explain RAG architecture",
            status="pending",
        )

        session.add(job)
        session.flush()

        job_id = job.id

        session.commit()

        print("Created user ID:", user_id)
        print("Created job ID:", job_id)

    # -----------------------------------
    # READ
    # -----------------------------------

    print("\n2. READ USER AND JOB")

    with SessionLocal() as session:

        stored_user = session.get(User, user_id)
        stored_job = session.get(Job, job_id)

        assert stored_user is not None
        assert stored_job is not None

        print("Username:", stored_user.username)
        print("Job topic:", stored_job.topic)
        print("Job status:", stored_job.status)

        user_jobs = session.scalars(
            select(Job).where(
                Job.user_id == user_id
            )
        ).all()

        print("Jobs owned by user:", len(user_jobs))

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    print("\n3. UPDATE JOB")

    with SessionLocal() as session:

        stored_job = session.get(Job, job_id)

        assert stored_job is not None

        stored_job.status = "completed"
        stored_job.result = (
            "Demo result: RAG combines retrieval "
            "with generation."
        )

        session.commit()

        print("Job update committed")

    # -----------------------------------
    # VERIFY UPDATE
    # -----------------------------------

    with SessionLocal() as session:

        stored_job = session.get(Job, job_id)

        assert stored_job is not None
        assert stored_job.status == "completed"

        print("Updated status:", stored_job.status)
        print("Updated result:", stored_job.result)

    # -----------------------------------
    # ROLLBACK
    # -----------------------------------

    print("\n4. TEST TRANSACTION ROLLBACK")

    with SessionLocal() as session:

        stored_job = session.get(Job, job_id)

        assert stored_job is not None

        stored_job.status = "failed"

        session.flush()

        print("Temporary status:", stored_job.status)

        session.rollback()

        print("Transaction rolled back")

    with SessionLocal() as session:

        stored_job = session.get(Job, job_id)

        assert stored_job is not None
        assert stored_job.status == "completed"

        print("Status after rollback:", stored_job.status)

    # -----------------------------------
    # DELETE
    # -----------------------------------

    print("\n5. DELETE DEMO JOB AND USER")

    with SessionLocal() as session:

        stored_job = session.get(Job, job_id)
        stored_user = session.get(User, user_id)

        assert stored_job is not None
        assert stored_user is not None

        # Delete the child record first.
        session.delete(stored_job)
        session.flush()

        # Delete the parent record next.
        session.delete(stored_user)

        session.commit()

        print("Demo records deleted")

    # -----------------------------------
    # VERIFY DELETION
    # -----------------------------------

    with SessionLocal() as session:

        assert session.get(Job, job_id) is None
        assert session.get(User, user_id) is None

        print("Deletion verified")

    print("\nALL CRUD AND TRANSACTION TESTS PASSED")


if __name__ == "__main__":
    main()
