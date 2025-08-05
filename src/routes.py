from fastapi import APIRouter, Query
from typing import List, Optional
from .models.book import Book
from .services.books import (
    list_books,
    search_books_service,
    get_book_by_id_service,
    get_top_rated_books,
    get_books_by_price_range,
)
from .services.categories import list_categories_service
from .services.health import health_check_service

router = APIRouter()


@router.get(
    "/api/v1/health",
    summary="Verifica a saúde da API"
)
async def health_check():
    return health_check_service()


@router.get(
    "/api/v1/books",
    response_model=List[Book],
    summary="Lista todos os livros",
)
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
):
    return list_books(limit=limit, offset=offset)


@router.get(
    "/api/v1/books/search",
    response_model=List[Book],
    summary="Busca livros por título e/ou categoria",
)
async def search_books(
    title: Optional[str] = Query(
        None, description="Título (parcial ou exato) do livro para buscar."
    ),
    category: Optional[str] = Query(None, description="Categoria do livro para buscar."),
):
    return search_books_service(title=title, category=category)


@router.get(
    "/api/v1/books/top-rated",
    response_model=List[Book],
    summary="Lista os livros com melhor avaliação",
)
async def get_top_rated_books_route(limit: int = Query(10, ge=1, le=100)):
    return get_top_rated_books(limit)


@router.get(
    "/api/v1/books/price-range",
    response_model=List[Book],
    summary="Filtra livros por faixa de preço",
)
async def get_books_by_price_range_route(
    min: float = Query(0.0, ge=0.0, le=100), max: float = Query(10.0, ge=1.0, le=1000.0), limit: int = Query(10, ge=1, le=100)
):
    return get_books_by_price_range(min_price=min, max_price=max, limit=limit)


@router.get(
    "/api/v1/books/{book_id}",
    response_model=Book,
    summary="Obtém detalhes de um livro por ID",
)
async def get_book_by_id(book_id: int):
    return get_book_by_id_service(book_id)


@router.get(
    "/api/v1/categories",
    summary="Lista todas as categorias de livros únicas",
)
async def get_all_categories():
    return {"categories": list_categories_service()}
