from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg:///genai_day37_new"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)