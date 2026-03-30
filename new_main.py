from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from typing import List

app = FastAPI()

class Book(BaseModel):
    id: int
    name: str

books = [
    {"id": 1, "name": "The Great Gatsby"},
    {"id": 2, "name": "To Kill a Mockingbird"},
    {"id": 3, "name": "1984"},
    {"id": 4, "name": "Pride and Prejudice"}
]

@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@app.get("/books/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_data: Book) -> dict:
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = updated_data.model_dump()
            return books[index]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int) -> dict:
    for index, book in enumerate(books):
        if book["id"] == book_id:
            deleted_book = books.pop(index)
            return {"message": "Book deleted", "book": deleted_book}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")