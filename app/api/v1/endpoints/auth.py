"""Authentication endpoints – login, token refresh, API-key info."""
import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import settings
from app.dependencies import get_current_user
from app.schemas.auth import LoginRequest, Token, UserInfo
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/login", response_model=Token, summary="Login and obtain JWT token")
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Authenticate with username/password and return a JWT access token."""
    user = await auth_service.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_service.create_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserInfo, summary="Get current user info")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return information about the currently authenticated user."""
    return UserInfo(
        username=current_user.get("sub", "unknown"),
        role=current_user.get("role", "user"),
    )
