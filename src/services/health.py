import logging
from fastapi import HTTPException, status
from .database import load_books_df

logger = logging.getLogger("uvicorn.error")

def health_check_service():
    logger.info("Verificando saúde da API e disponibilidade dos dados.")
    df = load_books_df()
    if df.empty:
        logger.error('Dados dos livros não carregados ou indisponíveis.')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Dados dos livros não carregados ou indisponíveis.')
    logger.debug('API saudável e dados carregados.')
    return {'status': 'OK', 'message': 'API funcionando e dados carregados.'}
