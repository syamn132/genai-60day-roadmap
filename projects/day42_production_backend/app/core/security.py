
import os

from datetime import datetime, timedelta, timezone

import jwt

from pwdlib import PasswordHash


# Password hashing configuration
password_hasher = PasswordHash.recommended()


# JWT configuration
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)


def verify_password(
    plain_password: str,
    stored_hash: str,
) -> bool:
    return password_hasher.verify(
        plain_password,
        stored_hash,
    )


def get_jwt_secret() -> str:

    secret = os.getenv("JWT_SECRET_KEY")

    if not secret or len(secret) < 32:
        raise RuntimeError(
            "JWT_SECRET_KEY must be set "
            "to a strong secret"
        )

    return secret


def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> str:

    now = datetime.now(timezone.utc)

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(
        payload,
        get_jwt_secret(),
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:

    return jwt.decode(
        token,
        get_jwt_secret(),
        algorithms=[JWT_ALGORITHM],
        options={
            "require": ["sub", "iat", "exp"]
        },
    )
