from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.services.books import get_db
from src.services.auth import (
    register_user_service,
    login_service,
    refresh_token_service
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", summary="Cria um novo usuário")
def register_user(
    username: str,
    password: str,
    confirm_pessword: str,
    fullname: str,
    cellphone: str,
    db: Session = Depends(get_db)
):
    return register_user_service(username, password, confirm_pessword, fullname, cellphone, db)

@router.post("/login", summary="Realiza login e retorna token JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_service(form_data, db)

@router.post("/refresh", summary="Renova o token JWT")
def refresh_token(token: str):
    return refresh_token_service(token)