"""Clients CRUD – raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import ClientCreate, ClientUpdate

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.get("")
def list_clients(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM clients ORDER BY created_at DESC")


@router.post("")
def create_client(body: ClientCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    return execute_returning(conn,
        "INSERT INTO clients (company_name, industry, description, icon) VALUES (%s,%s,%s,%s) RETURNING *",
        (body.companyName, body.industry, body.description, body.icon)
    )


@router.put("/{item_id}")
def update_client(item_id: int, body: ClientUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM clients WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Client not found")
    payload = body.model_dump(exclude_unset=True)
    return execute_returning(conn,
        "UPDATE clients SET company_name=COALESCE(%s,company_name), industry=COALESCE(%s,industry), description=COALESCE(%s,description), icon=COALESCE(%s,icon), updated_at=now() WHERE id=%s RETURNING *",
        (payload.get("companyName"), payload.get("industry"), payload.get("description"), payload.get("icon"), item_id)
    )


@router.delete("/{item_id}")
def delete_client(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM clients WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Client not found")
    execute(conn, "DELETE FROM clients WHERE id=%s", (item_id,))
    return {"message": "Client deleted"}
