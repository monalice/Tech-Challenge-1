import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.book_orm import BookORM

logger = logging.getLogger("uvicorn.error")

def list_categories_service(db: Session) -> list[str]:
    try:
        logger.info("Listando categorias únicas de livros.")
        categories = db.query(BookORM.category).distinct().all()
        categories = sorted([c[0] for c in categories if c[0]])
        logger.debug(f"Categorias encontradas: {categories}")
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {e}")