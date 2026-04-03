"""Pydantic schemas for authentication."""
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = {"json_schema_extra": {"example": {"username": "admin", "password": "secret"}}}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    username: str
    role: str
