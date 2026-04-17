"""
Authentication middleware using Supabase JWT.
"""
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config.database import get_supabase
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Dependency to verify Supabase JWT token and return the user.
    """
    token = credentials.credentials
    try:
        supabase = get_supabase()
        response = supabase.auth.get_user(jwt=token)
        if not response or not getattr(response, 'user', None):
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return response.user
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
