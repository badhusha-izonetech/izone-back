"""
Database layer using raw psycopg2 – bypasses SQLAlchemy ORM session
which has a greenlet incompatibility with Python 3.14.

Each request gets its own psycopg2 connection via get_db().
"""
import psycopg2
import psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool
from sqlalchemy.orm import declarative_base
from app.config import DATABASE_URL

# Build connection kwargs from DATABASE_URL
# Format: postgresql://user:password@host:port/dbname
import urllib.parse as _up

_parsed = _up.urlparse(DATABASE_URL)
_DB_PARAMS = dict(
    host=_parsed.hostname,
    port=_parsed.port or 5432,
    dbname=_parsed.path.lstrip("/"),
    user=_parsed.username,
    password=_parsed.password,
)

# Shared SQLAlchemy metadata for table creation scripts.
Base = declarative_base()

# Connection pool (min=1, max=10)
_pool = ThreadedConnectionPool(1, 10, **_DB_PARAMS)


def _snake_to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def _camelize(value):
    if isinstance(value, list):
        return [_camelize(item) for item in value]
    if isinstance(value, dict):
        return {_snake_to_camel(key): _camelize(val) for key, val in value.items()}
    return value


def get_raw_conn():
    """Get a raw psycopg2 connection from the pool."""
    return _pool.getconn()


def release_conn(conn):
    _pool.putconn(conn)


def get_db():
    """
    FastAPI dependency – yields a dict-cursor connection.
    Rows are returned as dicts with column-name keys.
    """
    conn = _pool.getconn()
    conn.autocommit = False
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


def fetchall(conn, query, params=None):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params or ())
        return [_camelize(dict(r)) for r in cur.fetchall()]


def fetchone(conn, query, params=None):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params or ())
        row = cur.fetchone()
        return _camelize(dict(row)) if row else None


def execute(conn, query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params or ())


def execute_returning(conn, query, params=None):
    """Execute INSERT/UPDATE with RETURNING and return first row as dict."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params or ())
        row = cur.fetchone()
        return _camelize(dict(row)) if row else None
