"""DB Playground – connect to any supported database and run ad-hoc queries."""
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.db_playground import (
    ComparisonRequest,
    ComparisonResponse,
    DBConnectionRequest,
    DBQueryRequest,
    DBQueryResponse,
)
from app.services.db_service import DBService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_db_service() -> DBService:
    return DBService()


@router.post(
    "/query",
    response_model=DBQueryResponse,
    summary="Run a query on a connected database",
)
async def run_query(
    request: DBQueryRequest,
    current_user: dict = Depends(get_current_user),
    db_service: DBService = Depends(get_db_service),
):
    """Execute a SQL query against the specified database engine."""
    result = await db_service.run_query(request)
    return result


@router.post(
    "/compare",
    response_model=ComparisonResponse,
    summary="Compare classified document data against a database",
)
async def compare_data(
    request: ComparisonRequest,
    current_user: dict = Depends(get_current_user),
    db_service: DBService = Depends(get_db_service),
):
    """Compare extracted/classified fields against records in an enterprise database."""
    result = await db_service.compare(request)
    return result


@router.post(
    "/test-connection",
    summary="Test connectivity to a database",
)
async def test_connection(
    request: DBConnectionRequest,
    current_user: dict = Depends(get_current_user),
    db_service: DBService = Depends(get_db_service),
):
    """Test whether a connection can be established to the given database."""
    ok = await db_service.test_connection(request)
    if ok:
        return {"status": "connected", "db_type": request.db_type}
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=f"Cannot connect to {request.db_type} database",
    )
