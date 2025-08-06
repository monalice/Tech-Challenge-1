from src.db.db import engine, Base
from src.models.book_orm import BookORM

def init_db():
    Base.metadata.create_all(bind=engine)
