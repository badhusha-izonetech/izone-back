"""Popups CRUD – public GET + admin CRUD using raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import PopupCreate, PopupUpdate

router = APIRouter(prefix="/api/popups", tags=["Popups"])


@router.get("")
def list_popups(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM popups ORDER BY created_at DESC")


@router.get("/active")
def get_active_popup(conn=Depends(get_db)):
    return fetchone(conn, "SELECT * FROM popups WHERE is_active = TRUE LIMIT 1")


@router.post("")
def create_popup(body: PopupCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if body.isActive:
        execute(conn, "UPDATE popups SET is_active = FALSE WHERE is_active = TRUE")
    row = execute_returning(conn,
        "INSERT INTO popups (title, description, is_active, image) VALUES (%s, %s, %s, %s) RETURNING *",
        (body.title, body.description, body.isActive, body.image)
    )
    return row


@router.put("/{popup_id}")
def update_popup(popup_id: int, body: PopupUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    row = fetchone(conn, "SELECT id FROM popups WHERE id = %s", (popup_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Popup not found")
    payload = body.model_dump(exclude_unset=True)
    if payload.get("isActive") is True:
        execute(conn, "UPDATE popups SET is_active = FALSE WHERE id <> %s AND is_active = TRUE", (popup_id,))
    updated = execute_returning(conn,
        "UPDATE popups SET title=COALESCE(%s,title), description=COALESCE(%s,description), is_active=COALESCE(%s,is_active), image=COALESCE(%s,image), updated_at=now() WHERE id=%s RETURNING *",
        (payload.get("title"), payload.get("description"), payload.get("isActive"), payload.get("image"), popup_id)
    )
    return updated


@router.delete("/{popup_id}")
def delete_popup(popup_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    row = fetchone(conn, "SELECT id FROM popups WHERE id = %s", (popup_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Popup not found")
    execute(conn, "DELETE FROM popups WHERE id = %s", (popup_id,))
    return {"message": "Popup deleted"}
