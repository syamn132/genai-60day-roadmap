
from datetime import datetime

from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class JobCreate(BaseModel):

    topic: str = Field(
        min_length=3,
        max_length=200,
    )


class JobPublic(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    user_id: int
    topic: str
    status: str
    result: str | None
    created_at: datetime


class JobStatusPublic(BaseModel):

    job_id: int

    status: Literal[
        "pending",
        "running",
        "completed",
        "failed",
    ]

    result: str | None

    source: Literal[
        "redis",
        "postgresql",
    ]
