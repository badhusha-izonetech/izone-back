import sys
from sqlalchemy import create_engine

from app.config import DATABASE_URL
from app.database import Base
from app import models  # noqa: F401 - registers model metadata
from app.schema_bootstrap import ensure_database_schema

engine = create_engine(DATABASE_URL, echo=True)

try:
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    ensure_database_schema()
    print("SUCCESS: Tables created!")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
