"""
API route handlers for the Bookstore API

Why separate from main.py?
- As APIs grow, you'd have routes/, models/, services/
- Each resource (books, authors, orders) gets its own file
- Easier testing: import routes without starting server
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models import Book, BookCreate, BookUpdate
from app.database import db

# Create a router (sub-application)
# In larger apps, you'd have: books_router, authors_router, etc.
router = APIRouter(
    prefix="/books",
    tags=["books"],  # Groups endpoints in auto-generated docs
)


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Add a new book to the bookstore. ID is auto-generated."
)
def create_book(book: BookCreate):
    """
    Create a new book with the following information:

    - **title**: Book title (required, 1-200 chars)
    - **author**: Author name (required, 1-100 chars)
    - **price**: Price in USD (required, must be positive)
    - **available**: Availability (optional, defaults to true)

    Returns the created book with its assigned ID.
    """
    new_book = db.create(book)
    return new_book


@router.get(
    "/",
    response_model=List[Book],
    status_code=status.HTTP_200_OK,
    summary="Get all books",
    description="Retrieve a list of all books in the bookstore."
)
def get_books():
    """
    Retrieve all books from the database.

    Interview tip: "In production, I'd implement pagination:
    - Query params: ?page=1&limit=20
    - Response headers: X-Total-Count, Link (for next/prev pages)
    - Consider cursor-based pagination for large datasets"
    """
    return db.get_all()


@router.get(
    "/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    summary="Get a book by ID",
    description="Retrieve a specific book using its unique identifier."
)
def get_book(book_id: int):
    """
    Retrieve a single book by ID.

    - **book_id**: Unique identifier (path parameter)

    Returns 404 if book doesn't exist.
    """
    book = db.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book


@router.put(
    "/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    summary="Update a book",
    description="Update all fields of an existing book."
)
def update_book(book_id: int, book: BookUpdate):
    """
    Update an existing book (partial update supported).

    - **book_id**: ID of book to update
    - Provide only fields you want to change

    Interview distinction:
    - PUT: Traditionally replaces entire resource
    - PATCH: Partial update (what we're implementing)
    - This endpoint accepts partial updates, so PATCH might be more RESTful
    """
    updated_book = db.update(book_id, book)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return updated_book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Remove a book from the bookstore."
)
def delete_book(book_id: int):
    """
    Delete a book by ID.

    Returns:
    - 204 No Content: Successfully deleted (no body returned)
    - 404 Not Found: Book doesn't exist

    Interview tip: "204 is correct for DELETE - no response body needed.
    Some APIs return 200 with confirmation message, but 204 is more RESTful."
    """
    success = db.delete(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    # FastAPI automatically returns 204 with no content
    return None