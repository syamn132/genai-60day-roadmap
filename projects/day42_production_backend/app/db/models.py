
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Identity,
    String,
    Text,
    func,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


# ----------------------------------
# BASE CLASS
# ----------------------------------

class Base(DeclarativeBase):
    pass


# ----------------------------------
# USER MODEL
# ----------------------------------

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    jobs: Mapped[list["Job"]] = relationship(
        back_populates="user",
    )


# ----------------------------------
# JOB MODEL
# ----------------------------------

class Job(Base):

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="pending",
    )

    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="jobs",
    )
