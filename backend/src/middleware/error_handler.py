"""
Middleware components for FastAPI application.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
import logging
import traceback
from typing import Callable

logger = logging.getLogger(__name__)


from starlette.middleware.base import BaseHTTPMiddleware

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for handling and logging errors."""

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "details": str(e) if logger.level == logging.DEBUG else None
                }
            )


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable):
        logger.info(f"-> {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        logger.info(f"<- {request.method} {request.url.path} {response.status_code}")
        return response


def setup_exception_handlers(app):
    """Setup custom exception handlers."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors."""
        logger.warning(f"Validation error on {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation error",
                "details": jsonable_encoder(exc.errors())
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "details": str(exc) if logger.level == logging.DEBUG else None
            }
        )