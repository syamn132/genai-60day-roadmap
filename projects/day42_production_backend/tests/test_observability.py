
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_unique_request_ids():

    first = client.get("/health/live")
    second = client.get("/health/live")

    first_id = first.headers["x-request-id"]
    second_id = second.headers["x-request-id"]

    assert first.status_code == 200
    assert second.status_code == 200

    assert len(first_id) == 32
    assert first_id != second_id


def test_prometheus_metrics():

    client.get("/health/live")

    response = client.get("/metrics")

    assert response.status_code == 200

    assert "day42_http_requests_total" in response.text
    assert "day42_http_request_duration_seconds" in response.text

    assert (
        'route="/health/live"'
        in response.text
    )


def test_401_and_404_responses():

    unauthorized = client.get("/auth/me")

    assert unauthorized.status_code == 401

    assert (
        unauthorized.headers["www-authenticate"]
        == "Bearer"
    )

    assert (
        unauthorized.json()["request_id"]
        == unauthorized.headers["x-request-id"]
    )

    missing = client.get("/nonexistent-path")

    assert missing.status_code == 404
    assert missing.json()["detail"] == "Not Found"


def test_422_validation_response():

    response = client.post(
        "/auth/register",
        json={
            "username": "ab",
            "password": "a-long-demo-password",
        },
    )

    assert response.status_code == 422

    assert "detail" in response.json()

    assert (
        response.json()["request_id"]
        == response.headers["x-request-id"]
    )


def test_unexpected_500_is_safe():

    def broken_endpoint():
        raise RuntimeError(
            "private internal debug information"
        )

    app.add_api_route(
        "/__test_unexpected_error",
        broken_endpoint,
        methods=["GET"],
        include_in_schema=False,
    )

    test_route = app.router.routes[-1]

    try:

        response = client.get(
            "/__test_unexpected_error"
        )

        assert response.status_code == 500

        assert (
            response.json()["detail"]
            == "Internal server error"
        )

        assert (
            "private internal debug information"
            not in response.text
        )

        assert (
            response.json()["request_id"]
            == response.headers["x-request-id"]
        )

    finally:
        app.router.routes.remove(test_route)


def test_database_503_is_safe():

    def simulate_database_outage():

        raise OperationalError(
            "SELECT 1",
            {},
            Exception("Simulated database outage"),
        )

    app.add_api_route(
        "/__test_database_outage",
        simulate_database_outage,
        methods=["GET"],
        include_in_schema=False,
    )

    test_route = app.router.routes[-1]

    try:

        response = client.get(
            "/__test_database_outage"
        )

        assert response.status_code == 503

        assert (
            response.json()["detail"]
            == "Database temporarily unavailable"
        )

        assert (
            "Simulated database outage"
            not in response.text
        )

        assert (
            response.json()["request_id"]
            == response.headers["x-request-id"]
        )

    finally:
        app.router.routes.remove(test_route)
