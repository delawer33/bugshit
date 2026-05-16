from collections import defaultdict
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import get_settings

settings = get_settings()
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

_query_cache: dict[str, list] = {}
_cache_hits = defaultdict(int)


def cache_query(key: str, rows: list) -> list:
    _query_cache[key] = rows
    _cache_hits[key] += 1
    return rows


def get_cached_query(key: str) -> list | None:
    return _query_cache.get(key)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY)"
            )
        )
        conn.commit()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
