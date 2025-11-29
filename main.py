# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 🎯 Step 1: Book model using Pydantic
class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    available: bool = True

# 🗃️ Step 2: In-memory database (list)
books: List[Book] = []

# 🏠 Welcome route
@app.get("/")
def home():
    return {"message": "📚 Welcome to the Bookstore API!"}

# 📖 Step 3: Get all books
@app.get("/books")
def get_books():
    return books

# 🔍 Step 4: Get a single book by ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# ➕ Step 5: Add a new book
@app.post("/books")
def add_book(book: Book):
    books.append(book)
    return {"message": "✅ Book added", "book": book}

# 📝 Step 6: Update a book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for idx, book in enumerate(books):
        if book.id == book_id:
            books[idx] = updated_book
            return {"message": "📝 Book updated", "book": updated_book}
    raise HTTPException(status_code=404, detail="Book not found")

# ❌ Step 7: Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "🗑️ Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")