"""
Izone Technologies – Backend API
FastAPI application entry point.
- All 14 routers registered
- CORS configured for production security
- Tables managed via init_tables.py (run once)
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.config import ALLOWED_ORIGINS, DEBUG
from app.schema_bootstrap import ensure_database_schema
from app.routers import (
    auth,
    popups,
    testimonials,
    job_roles,
    intern_roles,
    clients,
    team,
    contacts,
    job_applications,
    intern_applications,
    project_inquiries,
    site_photos,
    portfolios,
    dashboard,
)

# ── Logging ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ── App ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Izone Technologies API",
    description="Complete backend API for Izone Technologies website",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json" if DEBUG else None,  # Hide schema in production
)

# ── Security Headers Middleware ────────────────────────────────────────
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CSP: Stricter in production, permissive in development for Swagger UI
        if DEBUG:
            response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com"
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https:"
        
        return response

app.add_middleware(SecurityHeadersMiddleware)

# ── CORS ───────────────────────────────────────────────────────────────
allowed_origins_list = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# ── Routers ────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(popups.router)
app.include_router(testimonials.router)
app.include_router(job_roles.router)
app.include_router(intern_roles.router)
app.include_router(clients.router)
app.include_router(team.router)
app.include_router(contacts.router)
app.include_router(job_applications.router)
app.include_router(intern_applications.router)
app.include_router(project_inquiries.router)
app.include_router(site_photos.router)
app.include_router(portfolios.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def startup_ensure_schema():
    try:
        ensure_database_schema()
    except Exception as e:
        logger.error("Startup schema check failed: %s", e)


@app.get("/")
def root():
    return {"name": "Izone Technologies API", "version": "1.0.0", "docs": "/docs" if DEBUG else None}


@app.get("/api/health")
def health(conn=None):
    """Health check endpoint with database validation."""
    try:
        from app.database import get_raw_conn, release_conn
        test_conn = get_raw_conn()
        test_cursor = test_conn.cursor()
        test_cursor.execute("SELECT 1")
        test_cursor.close()
        release_conn(test_conn)
        logger.info("Health check: OK")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
