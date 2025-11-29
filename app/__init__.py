"""
Package initialization for the Bookstore API.
Goal: Make app/ a Python package

This file makes 'app/' a Python package, allowing imports like:
    from app.models import Book
    from app.database import db

Interview tip: "In larger projects, __init__.py can:
- Define package-level constants
- Initialize logging configuration
- Register plugins or extensions
- Set up package namespace"
"""

__version__ = "1.0.0"
__author__ = "Cody Chinothai"
__description__ = "Production-ready REST API for book management"