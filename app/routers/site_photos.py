"""Site Photos – raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import SitePhotoCreate

router = APIRouter(prefix="/api/site-photos", tags=["Site Photos"])


@router.get("")
def list_site_photos(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM site_photos ORDER BY created_at DESC")


@router.post("")
def create_site_photo(body: SitePhotoCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    return execute_returning(conn,
        "INSERT INTO site_photos (url, name, alt) VALUES (%s,%s,%s) RETURNING *",
        (body.url, body.name, body.alt)
    )


@router.delete("/{item_id}")
def delete_site_photo(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM site_photos WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Site photo not found")
    execute(conn, "DELETE FROM site_photos WHERE id=%s", (item_id,))
    return {"message": "Site photo deleted"}
