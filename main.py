from fastapi import FastAPI
from src.routes import router as books_router
import sys
import os
import logging

app = FastAPI(
    title="API Pública de Consulta de Livros",
    description="Uma API RESTful para consultar dados de livros extraídos de books.toscrape.com, pensada para engenheiros de Machine Learning.",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

@app.on_event("startup")
def run_scraper_on_startup():
    try:
        script_dir = os.path.join(os.path.dirname(__file__), "script")
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        from src.db.init_db import init_db
        init_db()
        from script.scraper_books import scrape_all_books, save_books_db
        books = scrape_all_books()
        save_books_db(books)
        logging.getLogger("uvicorn.error").info("Scraper executado com sucesso no startup.")
    except Exception as e:
        logging.getLogger("uvicorn.error").error(f"Erro ao executar scraper no startup: {e}")

app.include_router(books_router)
