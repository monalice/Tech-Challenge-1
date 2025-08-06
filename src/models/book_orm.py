from sqlalchemy import Column, Integer, String, Float
from ..db.db import Base

class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Integer, nullable=False)
    availability = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
