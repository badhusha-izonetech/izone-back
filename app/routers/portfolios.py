"""Portfolio Projects – raw psycopg2."""

import json
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import PortfolioCreate, PortfolioUpdate

router = APIRouter(prefix="/api/portfolios", tags=["Portfolios"])


@router.get("")
def list_portfolios(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM portfolios ORDER BY created_at DESC")


@router.get("/{item_id}")
def get_portfolio(item_id: int, conn=Depends(get_db)):
    row = fetchone(conn, "SELECT * FROM portfolios WHERE id=%s", (item_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return row


@router.post("")
def create_portfolio(body: PortfolioCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    return execute_returning(conn,
        "INSERT INTO portfolios (title, category, description, image, tags, client_name) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *",
        (body.title, body.category, body.description,
         body.image, json.dumps(body.tags), body.clientName)
    )


@router.put("/{item_id}")
def update_portfolio(item_id: int, body: PortfolioUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM portfolios WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Portfolio not found")
    payload = body.model_dump(exclude_unset=True)
    tags = payload.get("tags")
    tags_json = json.dumps(tags) if tags is not None else None
    return execute_returning(conn,
        "UPDATE portfolios SET title=COALESCE(%s,title), category=COALESCE(%s,category), description=COALESCE(%s,description), image=COALESCE(%s,image), tags=COALESCE(%s::jsonb,tags), client_name=COALESCE(%s,client_name), updated_at=now() WHERE id=%s RETURNING *",
        (payload.get("title"), payload.get("category"), payload.get("description"),
         payload.get("image"), tags_json, payload.get("clientName"), item_id)
    )


@router.delete("/{item_id}")
def delete_portfolio(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM portfolios WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Portfolio not found")
    execute(conn, "DELETE FROM portfolios WHERE id=%s", (item_id,))
    return {"message": "Portfolio deleted"}
