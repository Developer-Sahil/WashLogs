"""
Configuration module for WashLogs backend.
Handles environment variables and app settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings."""

    # API Configuration
    api_title: str = "WashLogs API"
    api_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Supabase Configuration
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    database_url: str

    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    def get_supabase_url(self) -> str:
        """Get Supabase URL."""
        return self.supabase_url

    def get_supabase_key(self) -> str:
        """Get Supabase anon key."""
        return self.supabase_anon_key

    def get_database_url(self) -> str:
        """Get database connection URL."""
        return self.database_url


# Load settings
settings = Settings()