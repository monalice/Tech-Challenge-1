import logging
from typing import List, Optional
from fastapi import HTTPException, status
from ..models.book import Book
from .database import load_books_df

logger = logging.getLogger("uvicorn.error")

def get_int_idx(idx):
    try:
        return int(idx)
    except Exception:
        return int(idx.item()) if hasattr(idx, 'item') else idx

def get_books_df():
    df = load_books_df()
    if 'id' not in df.columns:
        df = df.reset_index()
    if df.empty:
        logger.error('DataFrame de livros está vazio.')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Dados dos livros não disponíveis.')
    return df

def list_books(limit: int = 10, offset: int = 0) -> List[Book]:
    logger.info(f"Listando livros: limit={limit}, offset={offset}")
    df = get_books_df()
    paginated_books = df.iloc[offset:offset+limit]
    result = []
    for idx, row in paginated_books.iterrows():
        row_dict = row.to_dict()
        row_dict['id'] = get_int_idx(idx) if 'id' not in row_dict else row_dict['id']
        row_dict = {str(k): v for k, v in row_dict.items()}
        result.append(Book(**row_dict))
    logger.debug(f"Livros retornados: {len(result)}")
    return result

def search_books_service(title: Optional[str] = None, category: Optional[str] = None) -> List[Book]:
    logger.info(f"Buscando livros: title={title}, category={category}")
    df = get_books_df()
    if title:
        df = df[df['title'].str.contains(title, case=False, na=False)]
    if category:
        df = df[df['category'].str.contains(category, case=False, na=False)]
    if df.empty and (title or category):
        logger.warning('Nenhum livro encontrado com os critérios fornecidos.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum livro encontrado com os critérios fornecidos.')
    result = []
    for idx, row in df.head(1000).iterrows():
        row_dict = row.to_dict()
        row_dict['id'] = get_int_idx(idx) if 'id' not in row_dict else row_dict['id']
        row_dict = {str(k): v for k, v in row_dict.items()}
        result.append(Book(**row_dict))
    logger.debug(f"Livros encontrados: {len(result)}")
    return result

def get_book_by_id_service(book_id: int) -> Book:
    logger.info(f"Buscando livro por ID: {book_id}")
    df = get_books_df()
    filtered = df[df['id'] == book_id]
    if filtered.empty:
        logger.error(f'Livro com ID {book_id} não encontrado.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Livro com ID "{book_id}" não encontrado.')
    row = filtered.iloc[0]
    row_dict = row.to_dict()
    row_dict['id'] = int(book_id)
    row_dict = {str(k): v for k, v in row_dict.items()}
    logger.debug(f"Livro encontrado: {row_dict}")
    return Book(**row_dict)

def get_top_rated_books(limit: int = 10) -> List[Book]:
    logger.info(f"Listando os {limit} livros com melhor avaliação.")
    df = get_books_df()
    top_books = df.sort_values(by="rating", ascending=False).head(limit)
    result = []
    for idx, row in top_books.iterrows():
        row_dict = row.to_dict()
        row_dict['id'] = get_int_idx(idx) if 'id' not in row_dict else row_dict['id']
        row_dict = {str(k): v for k, v in row_dict.items()}
        result.append(Book(**row_dict))
    logger.debug(f"Top-rated retornados: {len(result)}")
    return result

def get_books_by_price_range(min_price: float, max_price: float, limit: int = 100) -> List[Book]:
    logger.info(f"Filtrando livros por faixa de preço: min={min_price}, max={max_price}")
    df = get_books_df()
    filtered = df[(df['price'] >= min_price) & (df['price'] <= max_price)].head(limit)
    result = []
    for idx, row in filtered.iterrows():
        row_dict = row.to_dict()
        row_dict['id'] = get_int_idx(idx) if 'id' not in row_dict else row_dict['id']
        row_dict = {str(k): v for k, v in row_dict.items()}
        result.append(Book(**row_dict))
    logger.debug(f"Livros na faixa retornados: {len(result)}")
    return result
