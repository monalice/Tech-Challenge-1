import logging
from typing import List, Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..models.book import Book
from ..models.book_orm import BookORM
from ..db.db import SessionLocal

logger = logging.getLogger("uvicorn.error")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def list_books(db: Session, limit: int = 10, offset: int = 0) -> List[Book]:
    logger.info(f"Listando livros: limit={limit}, offset={offset}")
    books = db.query(BookORM).order_by(BookORM.id).offset(offset).limit(limit).all()
    result = [Book(**book.__dict__) for book in books]
    logger.debug(f"Livros retornados: {len(result)}")
    return result

def search_books_service(db: Session, title: Optional[str] = None, category: Optional[str] = None) -> List[Book]:
    logger.info(f"Buscando livros: title={title}, category={category}")
    query = db.query(BookORM)
    if title:
        query = query.filter(BookORM.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(BookORM.category.ilike(f"%{category}%"))
    books = query.limit(1000).all()
    if not books and (title or category):
        logger.warning('Nenhum livro encontrado com os critérios fornecidos.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum livro encontrado com os critérios fornecidos.')
    result = [Book(**book.__dict__) for book in books]
    logger.debug(f"Livros encontrados: {len(result)}")
    return result

def get_top_rated_books(db: Session, limit: int = 10) -> List[Book]:
    logger.info(f"Listando os {limit} livros com melhor avaliação.")
    books = db.query(BookORM).order_by(BookORM.rating.desc()).limit(limit).all()
    result = [Book(**book.__dict__) for book in books]
    logger.debug(f"Top-rated retornados: {len(result)}")
    return result

def get_books_by_price_range(db: Session, min_price: float, max_price: float, limit: int = 100) -> List[Book]:
    logger.info(f"Filtrando livros por faixa de preço: min={min_price}, max={max_price}")
    books = db.query(BookORM).filter(BookORM.price >= min_price, BookORM.price <= max_price).limit(limit).all()
    result = [Book(**book.__dict__) for book in books]
    logger.debug(f"Livros na faixa retornados: {len(result)}")
    return result

def get_book_by_id_service(db: Session, book_id: int) -> Book:
    logger.info(f"Buscando livro por ID: {book_id}")
    book = db.query(BookORM).filter(BookORM.id == book_id).first()
    if not book:
        logger.error(f'Livro com ID {book_id} não encontrado.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Livro com ID "{book_id}" não encontrado.')
    logger.debug(f"Livro encontrado: {book.__dict__}")
    return Book(**book.__dict__)
