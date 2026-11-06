
from uuid import uuid4

import pytest

from fastapi.testclient import TestClient
from redis.exceptions import RedisError
from sqlalchemy import delete

from app.main import app
from app.db.models import Job, User
from app.db.session import SessionLocal, engine

from app.services import job_worker
from app.services.job_cache import (
    job_status_key,
    redis_client,
)

from redis.exceptions import ConnectionError as RedisConnectionError

from app.services import job_cache

TEST_DATABASE = "genai_day42_backend_test"

TEST_PASSWORD = "LocalE2ETestPassword_42!"

TEST_JWT_SECRET = (
    "day42-test-only-secret-" + "x" * 40
)


@pytest.fixture
def scenario(monkeypatch):

    # Protect the development database.
    if engine.url.database != TEST_DATABASE:
        pytest.skip(
            "E2E tests require the dedicated test database"
        )

    # Set a test-only JWT signing key.
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_JWT_SECRET,
    )

    # Avoid waiting four seconds per demo job.
    monkeypatch.setattr(
        job_worker.time,
        "sleep",
        lambda seconds: None,
    )

    # Give each test fresh user accounts.
    suffix = uuid4().hex[:10]

    usernames = [
        f"e2e_user_a_{suffix}",
        f"e2e_user_b_{suffix}",
    ]

    user_ids = []
    job_ids = []

    with TestClient(app) as client:

        try:

            # Create two users through the real API.
            for username in usernames:

                response = client.post(
                    "/auth/register",
                    json={
                        "username": username,
                        "password": TEST_PASSWORD,
                    },
                )

                assert response.status_code == 201, (
                    response.text
                )

                user_ids.append(response.json()["id"])

            # Log in each user through the real API.
            headers = []

            for username in usernames:

                response = client.post(
                    "/auth/login",
                    json={
                        "username": username,
                        "password": TEST_PASSWORD,
                    },
                )

                assert response.status_code == 200, (
                    response.text
                )

                token = response.json()["access_token"]

                headers.append(
                    {"Authorization": f"Bearer {token}"}
                )

            # Provide the prepared test scenario.
            yield {
                "client": client,
                "usernames": usernames,
                "user_ids": user_ids,
                "headers": headers,
                "job_ids": job_ids,
            }

        finally:

            # Clean up only users created by this fixture.
            if user_ids:

                with SessionLocal() as session:

                    session.execute(
                        delete(Job).where(
                            Job.user_id.in_(user_ids)
                        )
                    )

                    session.execute(
                        delete(User).where(
                            User.id.in_(user_ids)
                        )
                    )

                    session.commit()

            # Remove only the jobs' own Redis keys.
            for job_id in job_ids:

                try:
                    redis_client.delete(
                        job_status_key(job_id)
                    )

                except RedisError:
                    pass


def test_complete_successful_job_journey(scenario):

    client = scenario["client"]
    user_a_headers = scenario["headers"][0]

    response = client.post(
        "/jobs",
        headers=user_a_headers,
        json={
            "topic": "Explain transformer attention",
        },
    )

    assert response.status_code == 201

    created_job = response.json()
    job_id = created_job["id"]

    scenario["job_ids"].append(job_id)

    assert created_job["status"] == "pending"
    assert created_job["result"] is None

    # The test client completes the background task.
    details = client.get(
        f"/jobs/{job_id}",
        headers=user_a_headers,
    )

    assert details.status_code == 200
    assert details.json()["status"] == "completed"

    assert "Simulated AI response" in (
        details.json()["result"]
    )

    # Verify the Redis-backed status endpoint.
    status_response = client.get(
        f"/jobs/{job_id}/status",
        headers=user_a_headers,
    )

    assert status_response.status_code == 200

    assert status_response.json()["status"] == "completed"
    assert status_response.json()["source"] == "redis"

    # Verify the job appears in the owner's list.
    listing = client.get(
        "/jobs",
        headers=user_a_headers,
    )

    assert listing.status_code == 200

    assert any(
        job["id"] == job_id
        for job in listing.json()
    )


def test_failure_and_cross_user_protection(scenario):

    client = scenario["client"]

    user_a_headers = scenario["headers"][0]
    user_b_headers = scenario["headers"][1]

    response = client.post(
        "/jobs",
        headers=user_a_headers,
        json={"topic": "simulate_failure"},
    )

    assert response.status_code == 201

    job_id = response.json()["id"]
    scenario["job_ids"].append(job_id)

    # The background worker should record failure.
    details = client.get(
        f"/jobs/{job_id}",
        headers=user_a_headers,
    )

    assert details.status_code == 200
    assert details.json()["status"] == "failed"
    assert details.json()["result"] is None

    # User B cannot access User A's job.
    other_user_details = client.get(
        f"/jobs/{job_id}",
        headers=user_b_headers,
    )

    assert other_user_details.status_code == 404

    # Redis must not bypass ownership checks.
    other_user_status = client.get(
        f"/jobs/{job_id}/status",
        headers=user_b_headers,
    )

    assert other_user_status.status_code == 404

    # User B's job list must exclude User A's job.
    other_user_list = client.get(
        "/jobs",
        headers=user_b_headers,
    )

    assert other_user_list.status_code == 200

    assert all(
        job["id"] != job_id
        for job in other_user_list.json()
    )


def test_authentication_and_validation_boundaries(scenario):

    client = scenario["client"]
    username = scenario["usernames"][0]
    user_a_headers = scenario["headers"][0]

    # Correct token identifies the right account.
    me = client.get(
        "/auth/me",
        headers=user_a_headers,
    )

    assert me.status_code == 200
    assert me.json()["username"] == username

    # Duplicate username is rejected.
    duplicate = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": TEST_PASSWORD,
        },
    )

    assert duplicate.status_code == 409

    # Invalid registration data is rejected.
    invalid_registration = client.post(
        "/auth/register",
        json={
            "username": "ab",
            "password": TEST_PASSWORD,
        },
    )

    assert invalid_registration.status_code == 422

    # Wrong password is rejected.
    wrong_password = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "IncorrectPassword_42!",
        },
    )

    assert wrong_password.status_code == 401

    # Missing token is rejected.
    missing_token = client.get("/auth/me")

    assert missing_token.status_code == 401

    # Invalid token is rejected.
    invalid_token = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer not.a.valid.jwt"
        },
    )

    assert invalid_token.status_code == 401

    # Error responses carry a request ID.
    assert (
        invalid_token.json()["request_id"]
        == invalid_token.headers["x-request-id"]
    )


def test_redis_outage_falls_back_to_postgres(
    scenario,
    monkeypatch,
):

    client = scenario["client"]
    headers = scenario["headers"][0]

    # First, create a job with working services.
    response = client.post(
        "/jobs",
        headers=headers,
        json={
            "topic": "Explain embeddings"
        },
    )

    assert response.status_code == 201

    job_id = response.json()["id"]
    scenario["job_ids"].append(job_id)

    # Simulate a Redis connection failure.
    class UnavailableRedis:

        def get(self, key):
            raise RedisConnectionError(
                "Simulated Redis outage"
            )

        def set(self, *args, **kwargs):
            raise RedisConnectionError(
                "Simulated Redis outage"
            )

    monkeypatch.setattr(
        job_cache,
        "redis_client",
        UnavailableRedis(),
    )

    # The endpoint must fall back to PostgreSQL.
    response = client.get(
        f"/jobs/{job_id}/status",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "completed"
    assert data["source"] == "postgresql"
    assert "Simulated AI response" in data["result"]
