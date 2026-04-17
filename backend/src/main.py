"""
Main FastAPI application.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.config.database import init_supabase, init_database, close_db
from src.routes.order_controller import router as order_router, dashboard_router
from src.middleware.error_handler import setup_exception_handlers, LoggingMiddleware, ErrorHandlingMiddleware
from src.utils.helpers import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("============================================================")
    logger.info("[STARTUP] WashLogs Backend Starting...")
    logger.info("============================================================")
    
    try:
        init_supabase()
        init_database()
        logger.info("[SUCCESS] All services initialized")
    except Exception as e:
        logger.error(f"[ERROR] Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("============================================================")
    logger.info("[SHUTDOWN] WashLogs Backend Shutting Down...")
    logger.info("============================================================")
    close_db()
    logger.info("[SUCCESS] Services closed")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="A simple system for managing laundry/dry-cleaning orders",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(order_router)
app.include_router(dashboard_router)


# Health check endpoint
@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    responses={200: {"description": "Service is healthy"}}
)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    **Returns:**
    - status: "healthy"
    - service: "WashLogs API"
    """
    return {
        "status": "healthy",
        "service": "WashLogs API",
        "version": settings.api_version
    }


# Root endpoint
@app.get(
    "/",
    tags=["root"],
    summary="Welcome message",
    responses={200: {"description": "Welcome message"}}
)
async def root():
    """Welcome endpoint with API information."""
    return {
        "message": "Welcome to WashLogs API",
        "api_version": settings.api_version,
        "docs": "/api/docs",
        "endpoints": {
            "orders": {
                "create": "POST /api/orders",
                "list": "GET /api/orders",
                "get": "GET /api/orders/{order_id}",
                "update_status": "PATCH /api/orders/{order_id}/status",
                "delete": "DELETE /api/orders/{order_id}"
            },
            "dashboard": {
                "stats": "GET /api/dashboard"
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )