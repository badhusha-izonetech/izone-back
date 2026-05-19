"""Testimonials CRUD – raw psycopg2."""

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, fetchall, fetchone, execute_returning, execute
from app.auth import get_current_admin
from app.schemas import TestimonialCreate, TestimonialUpdate

router = APIRouter(prefix="/api/testimonials", tags=["Testimonials"])


@router.get("")
def list_testimonials(conn=Depends(get_db)):
    return fetchall(conn, "SELECT * FROM testimonials ORDER BY created_at DESC")


@router.post("")
def create_testimonial(body: TestimonialCreate, conn=Depends(get_db), _=Depends(get_current_admin)):
    return execute_returning(conn,
        "INSERT INTO testimonials (name, designation, description, rating, image) VALUES (%s,%s,%s,%s,%s) RETURNING *",
        (body.name, body.designation, body.description, body.rating, body.image)
    )


@router.put("/{item_id}")
def update_testimonial(item_id: int, body: TestimonialUpdate, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM testimonials WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Testimonial not found")
    payload = body.model_dump(exclude_unset=True)
    return execute_returning(conn,
        "UPDATE testimonials SET name=COALESCE(%s,name), designation=COALESCE(%s,designation), description=COALESCE(%s,description), rating=COALESCE(%s,rating), image=COALESCE(%s,image), updated_at=now() WHERE id=%s RETURNING *",
        (payload.get("name"), payload.get("designation"), payload.get("description"), payload.get("rating"), payload.get("image"), item_id)
    )


@router.delete("/{item_id}")
def delete_testimonial(item_id: int, conn=Depends(get_db), _=Depends(get_current_admin)):
    if not fetchone(conn, "SELECT id FROM testimonials WHERE id=%s", (item_id,)):
        raise HTTPException(status_code=404, detail="Testimonial not found")
    execute(conn, "DELETE FROM testimonials WHERE id=%s", (item_id,))
    return {"message": "Testimonial deleted"}
