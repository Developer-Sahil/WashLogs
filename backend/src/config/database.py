"""
Supabase database connection and initialization.
"""

from supabase import create_client, Client
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Generator
from src.config.settings import settings
from src.models.database import Base

logger = logging.getLogger(__name__)

# Global Supabase client
supabase_client: Client = None

# SQLAlchemy engine and session factory
engine = None
SessionLocal = None


def init_supabase() -> Client:
    """Initialize and return Supabase client."""
    global supabase_client
    try:
        supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        logger.info("Supabase client initialized successfully")
    except Exception as e:
        logger.warning(f"Using offline layout due to Supabase init error: {str(e)}")
        return supabase_client
    return supabase_client


def init_database() -> None:
    """Initialize database connection and create tables."""
    global engine, SessionLocal
    try:
        # Create engine with connection pooling
        engine = create_engine(
            settings.get_database_url(),
            poolclass=pool.QueuePool,
            pool_size=10,
            max_overflow=20,
            echo=settings.debug,
            pool_pre_ping=True  # Test connections before using them
        )
        
        # Create session factory
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("[SUCCESS] Database initialized successfully")
    except SQLAlchemyError as e:
        logger.error(f"[ERROR] Failed to initialize database: {str(e)}")
        raise


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def get_supabase() -> Client:
    """Get Supabase client instance."""
    if supabase_client is None:
        raise RuntimeError("Supabase client not initialized")
    return supabase_client


def close_db() -> None:
    """Close database connection."""
    if engine:
        engine.dispose()
        logger.info("[SUCCESS] Database connection closed")