"""Runtime-safe schema alignment for existing and fresh databases."""

import logging
import time
from sqlalchemy import create_engine

from app.config import SQLALCHEMY_DATABASE_URL
from app.database import Base
from app.database import get_raw_conn, release_conn
from app import models  # noqa: F401 - registers model metadata

logger = logging.getLogger(__name__)


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


def ensure_database_schema(retries: int = 5, delay: float = 3.0):
    """Create missing tables, then apply additive schema updates.
    Retries on connection failure to handle DB not-yet-ready on cold starts.
    """
    for attempt in range(1, retries + 1):
        try:
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            Base.metadata.create_all(bind=engine)
            engine.dispose()
            break
        except Exception as e:
            logger.warning("DB not ready (attempt %d/%d): %s", attempt, retries, e)
            if attempt == retries:
                logger.error("Could not reach database after %d attempts. Startup continuing without schema sync.", retries)
                return
            time.sleep(delay)

    conn = get_raw_conn()
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            for statement in SCHEMA_UPDATES:
                cur.execute(statement)
        logger.info("Database schema is up to date.")
    except Exception as e:
        logger.error("Schema update failed: %s", e)
    finally:
        release_conn(conn)
