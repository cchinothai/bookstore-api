"""
Pydantic models for the Bookstore API

Why separate models?
- BookBase: Shared fields (DRY principle)
- BookCreate: What users send (no ID)
- Book: What API returns (with ID)
- BookUpdate: Optional fields for PATCH (future-proofing)
"""

from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    """Shared properties across all book models"""
    title: str = Field(..., min_length=1, max_length=200,
                       description="Book title")
    author: str = Field(..., min_length=1, max_length=100,
                        description="Author name")
    price: float = Field(..., gt=0, description="Price must be positive")
    available: bool = Field(default=True, description="Availability status")


class BookCreate(BookBase):
    """
    Schema for creating a book.
    Notice: No 'id' field - server generates it!

    Interview tip: "Never trust client-provided IDs"
    """
    pass


class BookUpdate(BaseModel):
    """
    Schema for updating a book.
    All fields optional for partial updates (PATCH).

    Interview tip: "PUT replaces entire resource, PATCH updates parts"
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    available: Optional[bool] = None


class Book(BookBase):
    """
    Complete book representation with server-generated ID.
    This is what gets returned to clients.
    """
    id: int = Field(..., description="Unique book identifier")

    class Config:
        # Allows Pydantic to work with ORM objects (future SQLAlchemy integration)
        from_attributes = True
        # Example for API documentation
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "price": 29.99,
                "available": True
            }
        }