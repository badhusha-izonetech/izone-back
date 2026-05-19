"""Intern Roles CRUD – raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import InternRoleCreate

router = APIRouter(prefix="/api/intern-roles", tags=["Intern Roles"])


@router.get("")
def list_intern_roles(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM intern_roles ORDER BY created_at DESC")


@router.post("")
def create_intern_role(body: InternRoleCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    return execute_returning(conn,
        "INSERT INTO intern_roles (role_name) VALUES (%s) RETURNING *",
        (body.roleName,)
    )


@router.put("/{item_id}")
def update_intern_role(item_id: int, body: InternRoleCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM intern_roles WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Intern role not found")
    return execute_returning(conn,
        "UPDATE intern_roles SET role_name=%s WHERE id=%s RETURNING *",
        (body.roleName, item_id)
    )


@router.delete("/{item_id}")
def delete_intern_role(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM intern_roles WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Intern role not found")
    execute(conn, "DELETE FROM intern_roles WHERE id=%s", (item_id,))
    return {"message": "Intern role deleted"}
