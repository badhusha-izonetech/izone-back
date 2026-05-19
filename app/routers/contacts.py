"""Contacts – public POST + admin GET/mark-read/delete – raw psycopg2."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import ContactCreate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/contacts", tags=["Contacts"])


@router.get("")
def list_contacts(conn=Depends(get_db), _=Depends(get_current_admin)):
    try:
        items = fetchall(conn, "SELECT * FROM contacts ORDER BY created_at DESC")
        logger.info(f"Retrieved {len(items)} contacts")
        return items
    except Exception as e:
        logger.error(f"Error listing contacts: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve contacts")


@router.post("")
def create_contact(body: ContactCreate, conn=Depends(get_db)):
    try:
        result = execute_returning(conn,
            "INSERT INTO contacts (name, email, phone, subject, message) VALUES (%s,%s,%s,%s,%s) RETURNING *",
            (body.name, body.email, body.phone, body.subject, body.message)
        )
        logger.info(f"Created contact from {body.email}")
        return result
    except Exception as e:
        logger.error(f"Error creating contact: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create contact")


@router.patch("/{item_id}/read")
def mark_contact_read(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    try:
        if not fetchone(conn, "SELECT id FROM contacts WHERE id=%s", (item_id,)):
            raise HTTPException(status_code=404, detail="Contact not found")
        execute(conn, "UPDATE contacts SET is_read=TRUE WHERE id=%s", (item_id,))
        logger.info(f"Marked contact {item_id} as read")
        return {"message": "Marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking contact {item_id} as read: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update contact")


@router.delete("/{item_id}")
def delete_contact(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    try:
        if not fetchone(conn, "SELECT id FROM contacts WHERE id=%s", (item_id,)):
            raise HTTPException(status_code=404, detail="Contact not found")
        execute(conn, "DELETE FROM contacts WHERE id=%s", (item_id,))
        logger.info(f"Deleted contact {item_id}")
        return {"message": "Contact deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting contact {item_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete contact")
