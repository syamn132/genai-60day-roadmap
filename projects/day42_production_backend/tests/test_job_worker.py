
import pytest

from app.services import job_worker


def test_simulated_ai_response(monkeypatch):

    monkeypatch.setattr(
        job_worker.time,
        "sleep",
        lambda seconds: None,
    )

    result = job_worker.simulate_ai_response(
        "Explain RAG architecture"
    )

    assert "Explain RAG architecture" in result
    assert "Simulated AI response" in result


def test_simulated_ai_failure(monkeypatch):

    monkeypatch.setattr(
        job_worker.time,
        "sleep",
        lambda seconds: None,
    )

    with pytest.raises(
        RuntimeError,
        match="Intentional demo failure",
    ):
        job_worker.simulate_ai_response(
            "simulate_failure"
        )
