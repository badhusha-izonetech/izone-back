"""Team Members CRUD – raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import TeamMemberCreate, TeamMemberUpdate

router = APIRouter(prefix="/api/team", tags=["Team Members"])


@router.get("")
def list_team_members(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM team_members ORDER BY created_at DESC")


@router.post("")
def create_team_member(body: TeamMemberCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    return execute_returning(conn,
        "INSERT INTO team_members (name, role, avatar, bio) VALUES (%s,%s,%s,%s) RETURNING *",
        (body.name, body.role, body.avatar, body.bio)
    )


@router.put("/{item_id}")
def update_team_member(item_id: int, body: TeamMemberUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM team_members WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Team member not found")
    payload = body.model_dump(exclude_unset=True)
    return execute_returning(conn,
        "UPDATE team_members SET name=COALESCE(%s,name), role=COALESCE(%s,role), avatar=COALESCE(%s,avatar), bio=COALESCE(%s,bio), updated_at=now() WHERE id=%s RETURNING *",
        (payload.get("name"), payload.get("role"), payload.get("avatar"), payload.get("bio"), item_id)
    )


@router.delete("/{item_id}")
def delete_team_member(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM team_members WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Team member not found")
    execute(conn, "DELETE FROM team_members WHERE id=%s", (item_id,))
    return {"message": "Team member deleted"}
