"""
Main FastAPI application entry point

This file:
1. Creates the FastAPI app
2. Registers routers (like blueprints in Flask)
3. Adds middleware (CORS, logging, etc.)
4. Defines global exception handlers

Interview tip: "In microservices, each service would have its own
main.py. In monoliths, you'd have multiple routers imported here."
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import router as books_router

# Create the FastAPI application
app = FastAPI(
    title="Bookstore API",
    description="A production-ready REST API for managing books",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc alternative UI
)


# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for Pydantic validation errors.

    Why customize?
    - Cleaner error messages for clients
    - Consistent error response format
    - Hide internal details in production

    Interview tip: "In production, I'd log these errors to
    Sentry or CloudWatch for monitoring."
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "body": exc.body
        }
    )


# Global exception handler for HTTP errors
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Consistent format for all HTTP errors (404, 500, etc.)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Register routers (route modules)
app.include_router(books_router) # Adds all /books routes


# Root endpoint
@app.get("/", tags=["root"])
def read_root():
    """
    Health check / welcome endpoint.

    Interview tip: "In production APIs, I implement:
    - GET /health - for load balancers
    - GET /version - for deployment tracking
    - GET /metrics - for Prometheus monitoring"
    """
    return {
        "message": "📚 Welcome to the Bookstore API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "books": "/books",
            "health": "/health"
        }
    }


@app.get("/health", tags=["root"])
def health_check():
    """
    Health check endpoint for monitoring systems.

    In production, this would check:
    - Database connection
    - External API availability
    - Disk space, memory usage
    """
    return {
        "status": "healthy",
        "service": "bookstore-api"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Runs once when the server starts.

    Use cases:
    - Initialize database connections
    - Load ML models
    - Start background tasks
    - Warm up caches

    Interview tip: "I'd use this to create DB connection pools
    with SQLAlchemy or async drivers."
    """
    print("🚀 Bookstore API starting up...")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the server shuts down gracefully.

    Use cases:
    - Close database connections
    - Flush logs
    - Cancel background tasks
    - Save state
    """
    print("👋 Bookstore API shutting down...")


# For running with: python -m app.main
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Accept connections from any IP
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only!)
        log_level="info"
    )