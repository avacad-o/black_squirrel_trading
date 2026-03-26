"""
TimescaleDB connection and helpers. TPS § 1.11, 2.12.
"""
import os
from contextlib import contextmanager
from typing import Generator

# Optional: use psycopg2 or asyncpg. Stub with context manager.
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor  # type: ignore
    _HAS_PSYCOPG2 = True
except ImportError:
    psycopg2 = None  # type: ignore
    RealDictCursor = None  # type: ignore
    _HAS_PSYCOPG2 = False


def get_connection_string() -> str:
    return os.environ.get("TIMESCALE_URL", "postgresql://localhost:5432/black_squirrel")


@contextmanager
def get_conn() -> Generator:
    """Yield a connection; caller must not hold long. Use for short queries."""
    if not _HAS_PSYCOPG2:
        raise RuntimeError("Install psycopg2-binary for TimescaleDB support")
    conn = psycopg2.connect(get_connection_string())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute(sql: str, params: tuple | dict | None = None) -> None:
    """Execute one statement (no return)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())


def fetch_all(sql: str, params: tuple | dict | None = None) -> list[dict]:
    """Execute and return all rows as list of dicts."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            cols = [d[0] for d in cur.description] if cur.description else []
            return [dict(zip(cols, row)) for row in cur.fetchall()]
