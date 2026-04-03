"""Authentication service – user verification and token creation."""
import logging
from datetime import timedelta
from typing import Optional

from app.models.user import User
from app.utils.security import create_access_token, verify_password, get_password_hash

logger = logging.getLogger(__name__)

# In-memory user store – replace with a real DB in production
_USERS: dict = {
    "admin": User(
        username="admin",
        hashed_password=get_password_hash("secret"),
        role="admin",
        email="admin@example.com",
    ),
    "user": User(
        username="user",
        hashed_password=get_password_hash("password"),
        role="user",
        email="user@example.com",
    ),
}


class AuthService:
    async def authenticate_user(
        self, username: str, password: str
    ) -> Optional[dict]:
        user = _USERS.get(username)
        if user is None or user.disabled:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return {"username": user.username, "role": user.role}

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        return create_access_token(data, expires_delta)
