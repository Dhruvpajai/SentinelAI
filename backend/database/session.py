"""
SQLAlchemy database configuration.

Provides engine, session factory, and declarative base.
No table models are defined in Milestone 1.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.core.config import get_settings

settings = get_settings()

# SQLite requires check_same_thread=False for FastAPI async compatibility
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base for future ORM models."""


def get_db() -> Generator[Session, None, None]:
    """
    Yield a database session for dependency injection.

    Yields:
        SQLAlchemy Session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
