import logging
from typing import List
from fastapi import HTTPException, status
from .database import load_books_df

logger = logging.getLogger("uvicorn.error")

def get_books_df():
    df = load_books_df()
    if 'id' not in df.columns:
        df = df.reset_index()
    if df.empty:
        logger.error('DataFrame de livros está vazio.')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Dados dos livros não disponíveis.')
    return df

def list_categories_service() -> List[str]:
    logger.info("Listando categorias únicas de livros.")
    df = get_books_df()
    categories = sorted(df['category'].dropna().unique().tolist())
    logger.debug(f"Categorias encontradas: {categories}")
    return categories
