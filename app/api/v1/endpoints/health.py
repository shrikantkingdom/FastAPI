"""Health check endpoint."""
import logging
from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", summary="Health check", response_model=dict)
async def health_check():
    """Return application health status."""
    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
