"""In-memory user model (replace with ORM model for production persistence)."""
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str
    role: str = "user"
    disabled: bool = False
    email: Optional[str] = None
