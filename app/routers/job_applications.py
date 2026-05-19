"""Job Applications – public POST + admin GET/update/delete – raw psycopg2."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import JobApplicationCreate, JobApplicationUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/job-applications", tags=["Job Applications"])


@router.get("")
def list_job_applications(conn=Depends(get_db), _=Depends(get_current_admin)):
    try:
        items = fetchall(conn, "SELECT * FROM job_applications ORDER BY created_at DESC")
        logger.info(f"Retrieved {len(items)} job applications")
        return items
    except Exception as e:
        logger.error(f"Error listing job applications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve job applications")


@router.post("")
def create_job_application(body: JobApplicationCreate, conn=Depends(get_db)):
    try:
        result = execute_returning(conn,
            """INSERT INTO job_applications (name, email, phone, address, location, qualification, experience, message, resume, resume_name, resume_type, job_role)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
            (body.name, body.email, body.phone, body.address, body.location,
             body.qualification, body.experience,
             body.message, body.resume, body.resumeName, body.resumeType, body.jobRole)
        )
        logger.info(f"Created job application from {body.email} for role {body.jobRole}")
        return result
    except Exception as e:
        logger.error(f"Error creating job application: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create job application")


@router.patch("/{item_id}")
def update_job_application(item_id: int, body: JobApplicationUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    try:
        if not fetchone(conn, "SELECT id FROM job_applications WHERE id=%s", (item_id,)):
            raise HTTPException(status_code=404, detail="Job application not found")
        payload = body.model_dump(exclude_unset=True)
        result = execute_returning(conn,
            "UPDATE job_applications SET status=COALESCE(%s,status), is_read=COALESCE(%s,is_read) WHERE id=%s RETURNING *",
            (payload.get("status"), payload.get("isRead"), item_id)
        )
        logger.info(f"Updated job application {item_id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job application {item_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update job application")


@router.delete("/{item_id}")
def delete_job_application(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    try:
        if not fetchone(conn, "SELECT id FROM job_applications WHERE id=%s", (item_id,)):
            raise HTTPException(status_code=404, detail="Job application not found")
        execute(conn, "DELETE FROM job_applications WHERE id=%s", (item_id,))
        logger.info(f"Deleted job application {item_id}")
        return {"message": "Job application deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job application {item_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete job application")
