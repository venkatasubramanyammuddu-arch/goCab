from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config.settings import get_settings


def sqlalchemy_url(url: str) -> str:
    # SQLAlchemy picks the driver from the URL prefix; plain "postgresql://"
    # means the older psycopg2. We installed psycopg 3, so name it explicitly.
    return url.replace("postgresql://", "postgresql+psycopg://", 1)


# The engine owns a pool of connections to PostgreSQL.
# pool_pre_ping tests a connection before use, so a restarted database
# does not leave the app holding dead connections.
engine = create_engine(
    sqlalchemy_url(get_settings().database_url),
    pool_pre_ping=True,
)

# A session is one conversation with the database (a unit of work).
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Every table model inherits from this."""


def get_db() -> Iterator[Session]:
    # FastAPI dependency: one session per request, always closed afterwards.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
