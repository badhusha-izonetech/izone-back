"""Job Roles CRUD – raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import JobRoleCreate, JobRoleUpdate

router = APIRouter(prefix="/api/job-roles", tags=["Job Roles"])


@router.get("")
def list_job_roles(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM job_roles ORDER BY created_at DESC")


@router.get("/{item_id}")
def get_job_role(item_id: int, conn=Depends(get_db)):
    row = fetchone(conn, "SELECT * FROM job_roles WHERE id=%s", (item_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Job role not found")
    return row


@router.post("")
def create_job_role(body: JobRoleCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    return execute_returning(conn,
        "INSERT INTO job_roles (role_name, qualification, location, work_culture, work_timing, description, is_active) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *",
        (body.roleName, body.qualification, body.location,
         body.workCulture, body.workTiming, body.description, body.isActive)
    )


@router.put("/{item_id}")
def update_job_role(item_id: int, body: JobRoleUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM job_roles WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Job role not found")
    payload = body.model_dump(exclude_unset=True)
    return execute_returning(conn,
        "UPDATE job_roles SET role_name=COALESCE(%s,role_name), qualification=COALESCE(%s,qualification), location=COALESCE(%s,location), work_culture=COALESCE(%s,work_culture), work_timing=COALESCE(%s,work_timing), description=COALESCE(%s,description), is_active=COALESCE(%s,is_active), updated_at=now() WHERE id=%s RETURNING *",
        (payload.get("roleName"), payload.get("qualification"), payload.get("location"),
         payload.get("workCulture"), payload.get("workTiming"), payload.get("description"), payload.get("isActive"), item_id)
    )


@router.delete("/{item_id}")
def delete_job_role(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM job_roles WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Job role not found")
    execute(conn, "DELETE FROM job_roles WHERE id=%s", (item_id,))
    return {"message": "Job role deleted"}
