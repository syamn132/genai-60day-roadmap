
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.db.models import User
from app.db.session import get_session
from app.schemas.user import (
    UserRegister,
    UserPublic,
    UserLogin,
    TokenResponse,
)

import jwt

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserRegister,
    session: Annotated[Session, Depends(get_session)],
):

    existing_user = session.scalar(
        select(User).where(
            User.username == data.username
        )
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    user = User(
        username=data.username,
        password_hash=hash_password(
            data.password.get_secret_value()
        ),
    )

    session.add(user)

    try:
        session.commit()

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    session.refresh(user)

    return user


# ----------------------------------
# JWT LOGIN
# ----------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    data: UserLogin,
    session: Annotated[Session, Depends(get_session)],
):

    user = session.scalar(
        select(User).where(
            User.username == data.username
        )
    )

    if (
        user is None
        or not user.is_active
        or not verify_password(
            data.password.get_secret_value(),
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )


# ----------------------------------
# PROTECTED ROUTE DEPENDENCY
# ----------------------------------

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    session: Annotated[Session, Depends(get_session)],
) -> User:

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(
            credentials.credentials
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, ValueError, TypeError, KeyError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = session.get(User, user_id)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# ----------------------------------
# CURRENT USER ENDPOINT
# ----------------------------------

@router.get(
    "/me",
    response_model=UserPublic,
)
def read_current_user(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return current_user
