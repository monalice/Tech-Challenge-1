import logging
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.book_orm import BookORM

logger = logging.getLogger("uvicorn.error")

def list_categories_service(db: Session) -> List[str]:
    logger.info("Listando categorias únicas de livros.")
    categories = db.query(BookORM.category).distinct().all()
    categories = sorted([c[0] for c in categories if c[0]])
    logger.debug(f"Categorias encontradas: {categories}")
    return categories