from fastapi import APIRouter, Depends
from src.utils.auth import get_current_user
from src.services.scraping import trigger_scraping

router = APIRouter(prefix="/api/v1/scraping", tags=["scraping"])

@router.post("/trigger", summary="Executa o scraping manualmente (protegido por JWT)")
def trigger_scraping_route(user: str = Depends(get_current_user)):
    return trigger_scraping()