
# Day 42 — Production Backend Capstone

A multi-user FastAPI backend demonstrating PostgreSQL persistence,
SQLAlchemy ORM, Alembic migrations, JWT authentication, background
AI job processing, Redis caching, structured logging, Prometheus
metrics, and automated testing.

## Technology Stack

- Python 3.13
- FastAPI and Uvicorn
- PostgreSQL 17 and Psycopg
- SQLAlchemy 2
- Alembic
- Pydantic
- pwdlib / Argon2
- PyJWT
- Redis and redis-py
- Prometheus Python client
- pytest and HTTPX

## Implemented Features

1. Root and liveness endpoints.
2. User registration with password hashing.
3. JWT login and protected user profile.
4. Authenticated job creation and retrieval.
5. Job ownership enforcement.
6. Simulated background AI processing.
7. Pending, running, completed and failed job states.
8. Redis job-status caching with expiration.
9. PostgreSQL fallback when Redis is unavailable.
10. JSON logging, request IDs and Prometheus metrics.
11. Safe HTTP error handling.
12. Unit and end-to-end tests.

## Project Layout

app/
  main.py
  api/
    health.py
    auth.py
    jobs.py
  core/
    security.py
    logging_config.py
    metrics.py
    error_handlers.py
  db/
    session.py
    models.py
  schemas/
    user.py
    job.py
  services/
    job_worker.py
    job_cache.py

alembic/
tests/
requirements.txt
README.md

## Local Setup

From the roadmap root:

    source .venv/bin/activate
    cd projects/day42_production_backend

Install dependencies:

    python -m pip install -r requirements.txt

Ensure PostgreSQL and Redis are running:

    pg_isready
    redis-cli ping

Create the development database if it does not already exist:

    createdb genai_day42_backend

Apply database migrations:

    export DATABASE_URL="postgresql+psycopg:///genai_day42_backend"
    python -m alembic upgrade head

Set Redis configuration:

    export REDIS_URL="redis://127.0.0.1:6379/0"

Generate a local JWT secret:

    export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"

Never commit your real JWT secret to version control.
Changing the JWT secret invalidates existing access tokens.

Start the API:

    python -m uvicorn app.main:app --reload --port 8002

Swagger documentation:

    http://127.0.0.1:8002/docs

Metrics:

    http://127.0.0.1:8002/metrics

## Main Endpoints

GET  /                  Root information
GET  /health/live       Application liveness

POST /auth/register     Register user
POST /auth/login        Receive access token
GET  /auth/me           Read authenticated profile

POST /jobs              Create a job
GET  /jobs              List owned jobs
GET  /jobs/{job_id}     Retrieve an owned job
GET  /jobs/{job_id}/status
                         Retrieve cached or database status

GET  /metrics           Prometheus metrics

Authentication uses an HTTP Bearer token.

## Job Lifecycle

pending -> running -> completed

A processing failure results in:

pending -> running -> failed

The background worker uses a simulated AI response.
It does not call a real language model.

## Redis Cache

Job status entries use keys like:

    day42:job:7:status

The configured TTL is 60 seconds.

PostgreSQL remains the source of truth.

Ownership is checked in PostgreSQL before cached job
information is returned.

## Testing

Create a separate database for integration tests:

    createdb genai_day42_backend_test

Apply migrations to that database:

    DATABASE_URL="postgresql+psycopg:///genai_day42_backend_test" python -m alembic upgrade head

Run the complete suite:

    DATABASE_URL="postgresql+psycopg:///genai_day42_backend_test" REDIS_URL="redis://127.0.0.1:6379/0" python -m pytest -q

Expected after Part 6 implementation: 21 passing tests.

End-to-end tests create temporary users and jobs in the
dedicated test database and clean them up afterward.

## Observability

Each HTTP response includes an X-Request-ID header.

Application logs use JSON formatting.

Prometheus metrics track HTTP request counts, durations,
and completed or failed background jobs.

## Known Limitations

- BackgroundTasks is not a durable distributed queue.
- Server restarts can interrupt active background jobs.
- No automatic job retry or crash recovery yet.
- The AI response is simulated rather than model-generated.
- Redis is a cache, not the authoritative data store.
- Redis and PostgreSQL updates are not atomic.
- JWT token revocation and refresh tokens are not implemented.
- Public deployment requires HTTPS, rate limiting, and
  additional security controls.
- The metrics endpoint needs restricted network access
  before public deployment.
- Load testing and multi-worker deployment validation
  are not included.

## Learning Goal

This capstone integrates the backend engineering topics
covered in Days 35–41 of the 60-day Generative AI
Engineering roadmap.
