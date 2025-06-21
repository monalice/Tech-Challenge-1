import logging
from typing import List, Optional
from fastapi import HTTPException, status
from ..models import Book
from ..database import load_books_df

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
    if book_id not in df.index and (not (df['id'] == book_id).any()):
        logger.error(f'Livro com ID {book_id} não encontrado.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Livro com ID "{book_id}" não encontrado.')
    if book_id in df.index:
        row = df.loc[book_id]
    else:
        row = df[df['id'] == book_id].iloc[0]
    row_dict = row.to_dict()
    row_dict['id'] = int(book_id)
    row_dict = {str(k): v for k, v in row_dict.items()}
    logger.debug(f"Livro encontrado: {row_dict}")
    return Book(**row_dict)
