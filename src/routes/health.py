from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.health import health_check_service
from src.services.books import get_db

router = APIRouter(prefix="/api/v1/health", tags=["health"])

@router.get("", summary="Verifica a saúde da API")
async def health_check(db: Session = Depends(get_db)):
    return health_check_service(db=db)