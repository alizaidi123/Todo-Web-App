from sqlmodel import create_engine, Session
from typing import Generator
import os


# Use SQLite for development if no DATABASE_URL is provided
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE_URL") or "sqlite:///./todo_app.db"

# Create engine - use different settings for SQLite vs PostgreSQL
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Required for SQLite
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},  # Required for PostgreSQL/Neon
        pool_recycle=300,
        pool_pre_ping=True,
    )


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session