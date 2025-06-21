from fastapi import FastAPI
from src.routes import router as books_router

app = FastAPI(
    title="API Pública de Consulta de Livros",
    description="Uma API RESTful para consultar dados de livros extraídos de books.toscrape.com, pensada para engenheiros de Machine Learning.",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

app.include_router(books_router)
