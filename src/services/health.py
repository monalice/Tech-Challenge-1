import logging
from fastapi import HTTPException
from src.models.book_orm import BookORM
from sqlalchemy.orm import Session

logger = logging.getLogger("uvicorn.error")

def health_check_service(db: Session) -> dict:
    try:
        count = db.query(BookORM).count()
        return {"status": "ok", "books_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {e}")
