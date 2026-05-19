"""Intern Applications – public POST + admin GET/update/delete – raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import InternApplicationCreate, InternApplicationUpdate

router = APIRouter(prefix="/api/intern-applications", tags=["Intern Applications"])


@router.get("")
def list_intern_applications(conn=Depends(get_db), _=Depends(get_current_admin)):
    return fetchall(conn, "SELECT * FROM intern_applications ORDER BY created_at DESC")


@router.post("")
def create_intern_application(body: InternApplicationCreate, conn=Depends(get_db)):
    return execute_returning(conn,
        """INSERT INTO intern_applications (name, email, phone, role, address, qualification, skills, duration, message, resume, resume_name, resume_type)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
        (body.name, body.email, body.phone, body.role,
         body.address, body.qualification,
         body.skills, body.duration, body.message, body.resume, body.resumeName, body.resumeType)
    )


@router.patch("/{item_id}")
def update_intern_application(item_id: int, body: InternApplicationUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM intern_applications WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Intern application not found")
    payload = body.model_dump(exclude_unset=True)
    return execute_returning(conn,
        "UPDATE intern_applications SET status=COALESCE(%s,status), is_read=COALESCE(%s,is_read) WHERE id=%s RETURNING *",
        (payload.get("status"), payload.get("isRead"), item_id)
    )


@router.delete("/{item_id}")
def delete_intern_application(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM intern_applications WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Intern application not found")
    execute(conn, "DELETE FROM intern_applications WHERE id=%s", (item_id,))
    return {"message": "Intern application deleted"}
