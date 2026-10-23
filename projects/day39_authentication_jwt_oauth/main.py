from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
    Security,
)
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from jwt_utils import (
    create_access_token,
    verify_access_token,
)

from database import get_session
from models import User
from security import (
    DUMMY_HASH,
    hash_password,
    verify_password,
)


app = FastAPI(
    title="Day 39 - Authentication",
    version="1.0.0",
)

basic_security = HTTPBasic()

bearer_security = HTTPBearer(
    scheme_name="JWTBearer",
    bearerFormat="JWT",
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="oauth/demo-token",
    scheme_name="OAuth2Learning",
    scopes={
        "profile:read": "Read your own profile",
    },
)

DBSession = Annotated[
    Session,
    Depends(get_session),
]


# -------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------

class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
    )

    password: str = Field(
        min_length=12,
        max_length=128,
    )


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# -------------------------------------
# AUTHENTICATION HELPER
# -------------------------------------

def authenticate_user(
    username: str,
    password: str,
    session: Session,
) -> User | None:

    username = username.lower()

    statement = select(User).where(
        User.username == username
    )

    user = session.scalar(statement)

    if user is None:
        verify_password(password, DUMMY_HASH)
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    if not user.is_active:
        return None

    return user


def current_user(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(basic_security),
    ],
    session: DBSession,
) -> User:

    user = authenticate_user(
        credentials.username,
        credentials.password,
        session,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Basic"
            },
        )

    return user


# -------------------------------------
# PUBLIC ENDPOINT
# -------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------------------
# REGISTER USER
# -------------------------------------

@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    session: DBSession,
):
    username = data.username.lower()

    existing = session.scalar(
        select(User).where(
            User.username == username
        )
    )

    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    user = User(
        username=username,
        hashed_password=hash_password(
            data.password
        ),
        is_active=True,
    )

    session.add(user)

    try:
        session.commit()
        session.refresh(user)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
    )


# -------------------------------------
# VERIFY LOGIN CREDENTIALS
# -------------------------------------

@app.post("/login")
def login(
    user: Annotated[
        User,
        Depends(current_user),
    ],
):
    return {
        "message": "Authentication successful",
        "user_id": user.id,
        "username": user.username,
    }


# -------------------------------------
# PROTECTED ENDPOINT
# -------------------------------------

@app.get("/me", response_model=UserResponse)
def read_me(
    user: Annotated[
        User,
        Depends(current_user),
    ],
):
    return UserResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
    )

# -------------------------------------
# PART 2 — ISSUE JWT
# -------------------------------------

@app.post(
    "/jwt/token",
    response_model=TokenResponse,
)
def issue_jwt_token(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(basic_security),
    ],
    session: DBSession,
):

    user = authenticate_user(
        username=credentials.username,
        password=credentials.password,
        session=session,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    access_token = create_access_token(
        subject=str(user.id)
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )

# -------------------------------------
# PART 2 — VERIFY JWT AND LOAD USER
# -------------------------------------

def current_jwt_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_security),
    ],
    session: DBSession,
) -> User:

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        subject = verify_access_token(
            credentials.credentials
        )

        user_id = int(subject)

        if user_id <= 0 or str(user_id) != subject:
            raise ValueError("Invalid user ID")

    except ValueError:
        raise unauthorized

    user = session.get(User, user_id)

    if user is None or not user.is_active:
        raise unauthorized

    return user


# -------------------------------------
# PART 2 — JWT PROTECTED ENDPOINT
# -------------------------------------

@app.get(
    "/jwt/me",
    response_model=UserResponse,
)
def read_jwt_me(
    user: Annotated[
        User,
        Depends(current_jwt_user),
    ],
):

    return UserResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
    )


# -------------------------------------
# PART 3 — OAUTH2 LEARNING DEMO
# -------------------------------------

@app.post(
    "/oauth/demo-token",
    response_model=TokenResponse,
)
def issue_oauth_demo_token(
    form: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    session: DBSession,
):

    allowed_scopes = {"profile:read"}

    if not set(form.scopes).issubset(allowed_scopes):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported scope requested",
        )

    user = authenticate_user(
        username=form.username,
        password=form.password,
        session=session,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        subject=str(user.id),
        scopes=form.scopes,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )


# -------------------------------------
# VALIDATE OAUTH2 TOKEN + SCOPES
# -------------------------------------

def current_oauth_user(
    security_scopes: SecurityScopes,
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    session: DBSession,
) -> User:

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        subject = verify_access_token(
            token,
            required_scopes=security_scopes.scopes,
        )

        user_id = int(subject)

        if user_id <= 0 or str(user_id) != subject:
            raise ValueError("Invalid user ID")

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    except ValueError:
        raise unauthorized

    user = session.get(User, user_id)

    if user is None or not user.is_active:
        raise unauthorized

    return user


# -------------------------------------
# OAUTH2 PROTECTED ENDPOINT
# -------------------------------------

@app.get(
    "/oauth/me",
    response_model=UserResponse,
)
def oauth_read_me(
    user: Annotated[
        User,
        Security(
            current_oauth_user,
            scopes=["profile:read"],
        ),
    ],
):

    return UserResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
    )