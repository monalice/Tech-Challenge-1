from pydantic import BaseModel
from typing import List
from .book import Book

class BookListResponse(BaseModel):
    count: int
    books: List[Book]