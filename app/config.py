import os
from pathlib import Path

from dotenv import load_dotenv

# Load the backend-local .env even when the process starts from another directory.
# Real environment variables from Render or another host should take precedence.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


DATABASE_URL: str = _required_env("DATABASE_URL")
SQLALCHEMY_DATABASE_URL: str = (
    DATABASE_URL.replace("postgres://", "postgresql://", 1)
    if DATABASE_URL.startswith("postgres://")
    else DATABASE_URL
)
SECRET_KEY: str = _required_env("SECRET_KEY")  # MUST be set in production (32+ chars)
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
ADMIN_USERNAME: str = _required_env("ADMIN_USERNAME")  # MUST be set in production
ADMIN_PASSWORD: str = _required_env("ADMIN_PASSWORD")  # MUST be set in production
ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
