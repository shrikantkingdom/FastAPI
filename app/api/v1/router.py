"""API v1 router – aggregates all endpoint routers."""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, db_playground, documents, health

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, prefix="/health", tags=["Health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(
    documents.router, prefix="/documents", tags=["Document Processing"]
)
api_v1_router.include_router(
    db_playground.router, prefix="/db", tags=["DB Playground"]
)
