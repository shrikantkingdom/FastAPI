"""Database service – query execution and comparison logic."""
import logging
from typing import Any, Dict, List, Optional

from app.db.connectors import get_connector
from app.schemas.db_playground import (
    ComparisonRequest,
    ComparisonResponse,
    DBConnectionRequest,
    DBQueryRequest,
    DBQueryResponse,
    MismatchDetail,
)

logger = logging.getLogger(__name__)


class DBService:
    async def run_query(self, request: DBQueryRequest) -> DBQueryResponse:
        connector = get_connector(
            db_type=request.db_type,
            host=request.host,
            port=request.port,
            database=request.database,
            username=request.username,
            password=request.password,
        )
        try:
            columns, rows = connector.execute(request.query, request.params)
            return DBQueryResponse(
                db_type=request.db_type,
                query=request.query,
                columns=columns,
                rows=rows,
                row_count=len(rows),
            )
        except Exception as exc:
            logger.error(f"Query execution error: {exc}", exc_info=True)
            return DBQueryResponse(
                db_type=request.db_type,
                query=request.query,
                error=str(exc),
            )

    async def compare(self, request: ComparisonRequest) -> ComparisonResponse:
        connector = get_connector(
            db_type=request.db_type,
            host=request.host,
            port=request.port,
            database=request.database,
            username=request.username,
            password=request.password,
        )
        try:
            columns, rows = connector.execute(request.query)
            db_record: Optional[Dict[str, Any]] = None
            if rows:
                db_record = dict(zip(columns, rows[0]))

            mismatches: List[MismatchDetail] = []
            if db_record:
                for field, expected_value in request.classified_data.items():
                    actual = db_record.get(field)
                    if str(actual) != str(expected_value):
                        mismatches.append(
                            MismatchDetail(
                                field=field,
                                expected=expected_value,
                                actual=actual,
                            )
                        )

            return ComparisonResponse(
                match=len(mismatches) == 0,
                mismatches=mismatches,
                db_record=db_record,
                classified_data=request.classified_data,
            )
        except Exception as exc:
            logger.error(f"Comparison error: {exc}", exc_info=True)
            return ComparisonResponse(
                match=False,
                mismatches=[],
                db_record=None,
                classified_data=request.classified_data,
            )

    async def test_connection(self, request: DBConnectionRequest) -> bool:
        connector = get_connector(
            db_type=request.db_type,
            host=request.host,
            port=request.port,
            database=request.database,
            username=request.username,
            password=request.password,
        )
        return connector.test_connection()
