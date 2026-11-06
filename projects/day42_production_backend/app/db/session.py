
import os

from sqlalchemy import create_engine

from collections.abc import Iterator
from sqlalchemy.orm import Session, sessionmaker


# Read the database address from the environment.
DATABASE_URL = os.getenv("DATABASE_URL")


# Stop with a helpful error if the URL is missing.
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set"
    )


# Configure the SQLAlchemy Engine.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
