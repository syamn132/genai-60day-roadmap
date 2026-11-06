
from datetime import timedelta

import jwt
import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
)


TEST_SECRET = "day42-testing-only-" + "x" * 40


def test_valid_token(monkeypatch):

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET,
    )

    token = create_access_token(user_id=123)

    payload = decode_access_token(token)

    assert payload["sub"] == "123"


def test_expired_token(monkeypatch):

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET,
    )

    token = create_access_token(
        user_id=123,
        expires_delta=timedelta(seconds=-60),
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_tampered_token(monkeypatch):

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET,
    )

    token = create_access_token(user_id=123)

    parts = token.split(".")

    tampered_token = (
        parts[0] + "." +
        parts[1] + "." +
        "invalidsignature"
    )

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(tampered_token)
