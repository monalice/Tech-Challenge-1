from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.categories import list_categories_service
from src.services.books import get_db

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])

@router.get("/", summary="Lista todas as categorias de livros únicas")
async def get_all_categories(db: Session = Depends(get_db)):
    return {"categories": list_categories_service(db)}