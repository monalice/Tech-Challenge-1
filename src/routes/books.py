from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.book import Book
from src.services.books import (
    list_books,
    search_books_service,
    get_book_by_id_service,
    get_top_rated_books,
    get_books_by_price_range,
    get_db
)

router = APIRouter(prefix="/api/v1/books", tags=["books"])

@router.get("/", response_model=List[Book], summary="Lista todos os livros")
async def get_all_books(
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Número máximo de livros a retornar (padrão: 10, máximo: 100).",
    ),
    offset: int = Query(
        0, ge=0, description="Número de livros a pular (para paginação, padrão: 0)."
    ),
    db: Session = Depends(get_db)
):
    return list_books(db=db, limit=limit, offset=offset)


@router.get("/search", response_model=List[Book], summary="Busca livros por título e/ou categoria")
async def search_books(
    title: Optional[str] = Query(
        None, description="Título (parcial ou exato) do livro para buscar."
    ),
    category: Optional[str] = Query(None, description="Categoria do livro para buscar."),
    db: Session = Depends(get_db)
):
    return search_books_service(db=db, title=title, category=category)


@router.get("/top-rated", response_model=List[Book], summary="Lista os livros com melhor avaliação")
async def get_top_rated_books_route(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return get_top_rated_books(db=db, limit=limit)


@router.get("/price-range", response_model=List[Book], summary="Filtra livros por faixa de preço")
async def get_books_by_price_range_route(
    min: float = Query(0.0, ge=0.0, le=100), max: float = Query(10.0, ge=1.0, le=1000.0), limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_books_by_price_range(db=db, min_price=min, max_price=max, limit=limit)


@router.get("/{book_id}", response_model=Book, summary="Obtém detalhes de um livro por ID")
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return get_book_by_id_service(db=db, book_id=book_id)