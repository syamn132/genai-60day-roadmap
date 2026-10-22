from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import engine

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

DBSession = Annotated[Session, Depends(get_session)]