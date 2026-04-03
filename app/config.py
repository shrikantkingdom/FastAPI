"""Application configuration using Pydantic BaseSettings."""
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "FastAPI Backend Services"
    PROJECT_DESCRIPTION: str = (
        "Production-ready FastAPI backend with PDF processing, AI integration, "
        "and multi-database connectivity."
    )
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY_HEADER: str = "X-API-Key"
    VALID_API_KEYS: List[str] = ["dev-api-key-change-in-production"]

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # AI Provider
    AI_PROVIDER: str = "mock"  # "openai" | "mock"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Database connections (all optional - mocked when not provided)
    TERADATA_HOST: Optional[str] = None
    TERADATA_USERNAME: Optional[str] = None
    TERADATA_PASSWORD: Optional[str] = None
    TERADATA_DATABASE: Optional[str] = None

    DB2_HOST: Optional[str] = None
    DB2_PORT: int = 50000
    DB2_DATABASE: Optional[str] = None
    DB2_USERNAME: Optional[str] = None
    DB2_PASSWORD: Optional[str] = None

    SQLSERVER_HOST: Optional[str] = None
    SQLSERVER_PORT: int = 1433
    SQLSERVER_DATABASE: Optional[str] = None
    SQLSERVER_USERNAME: Optional[str] = None
    SQLSERVER_PASSWORD: Optional[str] = None

    # Configurable list of allowed base directories for server-side PDF access
    ALLOWED_PDF_DIRS: List[str] = ["/tmp/uploads", "/data/pdfs"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
