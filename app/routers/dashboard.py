"""Admin dashboard stats – raw psycopg2."""

from fastapi import APIRouter, Depends
from app.database import get_db, fetchone
from app.auth import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin Dashboard"])


def _count(conn, table: str, where: str = "") -> int:
    sql = f"SELECT COUNT(*) AS cnt FROM {table}"
    if where:
        sql += f" WHERE {where}"
    row = fetchone(conn, sql)
    return row["cnt"] if row else 0


@router.get("/stats")
def get_dashboard_stats(conn=Depends(get_db), _=Depends(get_current_admin)):
    return {
        "popups":             _count(conn, "popups"),
        "testimonials":       _count(conn, "testimonials"),
        "jobRoles":           _count(conn, "job_roles"),
        "internRoles":        _count(conn, "intern_roles"),
        "clients":            _count(conn, "clients"),
        "teamMembers":        _count(conn, "team_members"),
        "contacts":           _count(conn, "contacts"),
        "contactsUnread":     _count(conn, "contacts", "is_read = FALSE"),
        "jobApplications":    _count(conn, "job_applications"),
        "jobAppsPending":     _count(conn, "job_applications", "status = 'Pending'"),
        "internApplications": _count(conn, "intern_applications"),
        "internAppsPending":  _count(conn, "intern_applications", "status = 'Pending'"),
        "projectInquiries":   _count(conn, "project_inquiries"),
        "inquiriesNew":       _count(conn, "project_inquiries", "status = 'New'"),
        "sitePhotos":         _count(conn, "site_photos"),
        "portfolios":         _count(conn, "portfolios"),
    }
