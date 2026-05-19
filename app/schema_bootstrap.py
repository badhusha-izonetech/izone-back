"""Runtime-safe schema alignment for existing and fresh databases."""

from sqlalchemy import create_engine

from app.config import SQLALCHEMY_DATABASE_URL
from app.database import Base
from app.database import get_raw_conn, release_conn
from app import models  # noqa: F401 - registers model metadata


SCHEMA_UPDATES = [
    "ALTER TABLE popups ADD COLUMN IF NOT EXISTS image TEXT DEFAULT ''",
    "ALTER TABLE testimonials ADD COLUMN IF NOT EXISTS image TEXT DEFAULT ''",
    "ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS address TEXT DEFAULT ''",
    "ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS message TEXT DEFAULT ''",
    "ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS resume_type VARCHAR(255) DEFAULT ''",
    "ALTER TABLE intern_applications ADD COLUMN IF NOT EXISTS message TEXT DEFAULT ''",
    "ALTER TABLE intern_applications ADD COLUMN IF NOT EXISTS resume TEXT DEFAULT ''",
    "ALTER TABLE intern_applications ADD COLUMN IF NOT EXISTS resume_name VARCHAR(255) DEFAULT ''",
    "ALTER TABLE intern_applications ADD COLUMN IF NOT EXISTS resume_type VARCHAR(255) DEFAULT ''",
    "ALTER TABLE site_photos ADD COLUMN IF NOT EXISTS name VARCHAR(255) DEFAULT ''",
]


def ensure_database_schema():
    """Create missing tables, then apply additive schema updates."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    engine.dispose()

    conn = get_raw_conn()
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            for statement in SCHEMA_UPDATES:
                cur.execute(statement)
    finally:
        release_conn(conn)
