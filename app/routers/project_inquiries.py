"""Project Inquiries (GetStarted) – raw psycopg2."""

import json
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import ProjectInquiryCreate, ProjectInquiryUpdate

router = APIRouter(prefix="/api/project-inquiries", tags=["Project Inquiries"])


@router.get("")
def list_project_inquiries(conn=Depends(get_db), _=Depends(get_current_admin)):
    return fetchall(conn, "SELECT * FROM project_inquiries ORDER BY created_at DESC")


@router.post("")
def create_project_inquiry(body: ProjectInquiryCreate, conn=Depends(get_db)):
    return execute_returning(conn,
        """INSERT INTO project_inquiries (name, email, phone, company, selected_services, budget, timeline, project_details)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
        (body.name, body.email, body.phone, body.company,
         json.dumps(body.selectedServices), body.budget, body.timeline, body.projectDetails)
    )


@router.patch("/{item_id}")
def update_project_inquiry(item_id: int, body: ProjectInquiryUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM project_inquiries WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Project inquiry not found")
    payload = body.model_dump(exclude_unset=True)
    return execute_returning(conn,
        "UPDATE project_inquiries SET status=COALESCE(%s,status), is_read=COALESCE(%s,is_read) WHERE id=%s RETURNING *",
        (payload.get("status"), payload.get("isRead"), item_id)
    )


@router.delete("/{item_id}")
def delete_project_inquiry(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM project_inquiries WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Project inquiry not found")
    execute(conn, "DELETE FROM project_inquiries WHERE id=%s", (item_id,))
    return {"message": "Project inquiry deleted"}
