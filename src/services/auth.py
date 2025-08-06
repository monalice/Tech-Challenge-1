from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from src.models.user_orm import UserORM
from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def register_user_service(username: str, password: str, confirm_pessword: str, fullname: str, cellphone: str, db: Session):
    if db.query(UserORM).filter(UserORM.username == username).filter(UserORM.fullname == fullname).first():
        raise HTTPException(status_code=400, detail="Usuário já existe")
    if password != confirm_pessword:
        raise HTTPException(status_code=400, detail="Senhas não coincidem")
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres")
    if not username.isalnum():
        raise HTTPException(status_code=400, detail="O nome de usuário deve conter apenas caracteres alfanuméricos")
    if not fullname.replace(" ", "").isalpha():
        raise HTTPException(status_code=400, detail="O nome completo deve conter apenas letras")
    if not cellphone.isdigit() or len(cellphone) != 11:
        raise HTTPException(status_code=400, detail="O celular deve conter apenas números e ter 11 dígitos")
    user = UserORM(username=username, password=get_password_hash(password), fullname=fullname, cellphone=cellphone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

def login_service(form_data, db: Session):
    user = db.query(UserORM).filter(UserORM.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def refresh_token_service(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        new_token = create_access_token(data={"sub": username})
        return {"access_token": new_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")