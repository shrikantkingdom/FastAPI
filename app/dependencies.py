"""FastAPI dependency injection utilities."""
import logging
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader

from app.config import settings
from app.utils.security import decode_access_token

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)


async def get_current_user_from_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
) -> dict:
    """Validate JWT bearer token and return payload."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


async def get_current_user_from_api_key(
    api_key: Optional[str] = Security(api_key_header),
) -> dict:
    """Validate API key and return a minimal user dict."""
    import secrets

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    # Use constant-time comparison to prevent timing attacks
    if not any(secrets.compare_digest(api_key, valid) for valid in settings.VALID_API_KEYS):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return {"sub": "api-key-user", "auth_method": "api_key"}


async def get_current_user(
    token_user: Optional[dict] = Depends(get_current_user_from_token),
) -> dict:
    """Primary auth dependency – JWT token."""
    return token_user
