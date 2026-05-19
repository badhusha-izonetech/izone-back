"""Runtime-safe schema alignment for existing databases."""

from app.database import get_raw_conn, release_conn


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
    """Apply additive schema updates so the API stays compatible with the frontend."""
    conn = get_raw_conn()
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            for statement in SCHEMA_UPDATES:
                cur.execute(statement)
    finally:
        release_conn(conn)
