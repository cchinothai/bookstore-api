"""
In-memory database for the Bookstore API

Why a dictionary instead of a list?
- O(1) lookups by ID vs O(n) scanning
- More closely mirrors real databases (key-value)
- Easier to prevent duplicate IDs

Interview tip: "In production, this would be PostgreSQL with
SQLAlchemy ORM or an async driver like asyncpg"
"""

from typing import Dict, List, Optional
from app.models import Book, BookCreate, BookUpdate


class BookDatabase:
    """
    Encapsulates all data operations.

    Why a class?
    - Easy to swap with real DB later
    - Can add connection pooling, transactions
    - Testable with mock databases
    """

    def __init__(self):
        self._books: Dict[int, Book] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """
        Generate unique book ID.

        Production note: Real DBs handle this with AUTO_INCREMENT
        or SERIAL columns.
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def create(self, book_data: BookCreate) -> Book:
        """
        Create a new book with auto-generated ID.

        Args:
            book_data: Book info from user (no ID)

        Returns:
            Complete Book object with ID
        """
        book_id = self._generate_id()
        book = Book(
            id=book_id,
            **book_data.model_dump()  # Converts Pydantic model to dict
        )
        self._books[book_id] = book
        return book

    def get_all(self) -> List[Book]:
        """
        Retrieve all books.

        Interview tip: "In production, I'd add pagination to handle
        thousands of records: GET /books?page=1&limit=50"
        """
        return list(self._books.values())

    def get_by_id(self, book_id: int) -> Optional[Book]:
        """
        Retrieve a single book by ID.

        Returns:
            Book if found, None otherwise (cleaner than exceptions here)
        """
        return self._books.get(book_id)

    def update(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        """
        Update an existing book (partial update).

        Args:
            book_id: ID of book to update
            book_data: Fields to update (only non-None values)

        Returns:
            Updated book or None if not found
        """
        book = self._books.get(book_id)
        if not book:
            return None

        # Update only provided fields (exclude_unset=True)
        update_data = book_data.model_dump(exclude_unset=True)
        updated_book = book.model_copy(update=update_data)
        self._books[book_id] = updated_book

        return updated_book

    def delete(self, book_id: int) -> bool:
        """
        Delete a book by ID.

        Returns:
            True if deleted, False if not found
        """
        if book_id in self._books:
            del self._books[book_id]
            return True
        return False

    def exists(self, book_id: int) -> bool:
        """Check if a book exists"""
        return book_id in self._books

    def count(self) -> int:
        """Return total number of books"""
        return len(self._books)


# Global database instance
# In production with a real DB, this would be a connection pool
db = BookDatabase()