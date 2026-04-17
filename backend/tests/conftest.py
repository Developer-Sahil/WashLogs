import os
import pytest

# Inject environment variables before any application code is imported
# This ensures that Pydantic models in src.config.settings do not fail on startup.
os.environ["DEBUG"] = "true"
os.environ["ENVIRONMENT"] = "testing"
os.environ["SUPABASE_URL"] = "http://localhost:8000"
os.environ["SUPABASE_ANON_KEY"] = "dummy_key"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "dummy_service_key"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ALLOWED_ORIGINS"] = '["*"]'
os.environ["HOST"] = "127.0.0.1"
os.environ["PORT"] = "8000"
