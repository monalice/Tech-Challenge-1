from src.db.db import engine, Base
from src.models.book_orm import BookORM
from src.models.user_orm import UserORM

def init_db():
    Base.metadata.create_all(bind=engine)