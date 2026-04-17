"""
Utility functions and logging configuration.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from src.config.settings import settings


def setup_logging():
    """Configure logging for the application."""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "washlogs.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Environment: {settings.environment}")


class DatabaseHelper:
    """Database helper utilities."""

    @staticmethod
    def generate_pagination_metadata(total: int, limit: int, offset: int) -> dict:
        """Generate pagination metadata."""
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "pages": (total + limit - 1) // limit if limit > 0 else 0,
            "current_page": (offset // limit) + 1 if limit > 0 else 1
        }


class ValidationHelper:
    """Validation helper utilities."""

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format."""
        import re
        digits = re.sub(r'\D', '', phone)
        return len(digits) >= 10

    @staticmethod
    def is_valid_uuid(value: str) -> bool:
        """Validate UUID format."""
        import uuid
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False