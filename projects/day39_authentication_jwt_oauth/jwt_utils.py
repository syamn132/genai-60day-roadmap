import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    subject: str,
    expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    scopes: list[str] | None = None,
) -> str:

    if not subject:
        raise ValueError("Subject must not be empty")

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
        "scope": " ".join(scopes or []),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_access_token(
    token: str,
    required_scopes: list[str] | None = None,
) -> str:

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp"]},
        )

        subject = payload["sub"]

        if not isinstance(subject, str) or not subject:
            raise ValueError("Invalid token subject")

        raw_scopes = payload.get("scope", "")

        if not isinstance(raw_scopes, str):
            raise ValueError("Invalid token scopes")

        granted_scopes = set(raw_scopes.split())

        if not set(required_scopes or []).issubset(
            granted_scopes
        ):
            raise PermissionError(
                "Insufficient token scope"
            )

        return subject

    except (InvalidTokenError, ValueError) as exc:
        raise ValueError(
            "Invalid or expired access token"
        ) from exc