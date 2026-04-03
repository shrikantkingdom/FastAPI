"""Pydantic schemas for the DB playground."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DBConnectionRequest(BaseModel):
    db_type: str = Field(..., description="One of: teradata, db2, sqlserver")
    host: str
    port: Optional[int] = None
    database: str
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "db_type": "sqlserver",
                "host": "localhost",
                "port": 1433,
                "database": "mydb",
                "username": "sa",
                "password": "secret",
            }
        }
    }


class DBQueryRequest(BaseModel):
    db_type: str = Field(..., description="One of: teradata, db2, sqlserver")
    host: str
    port: Optional[int] = None
    database: str
    username: str
    password: str
    query: str = Field(..., description="SQL query to execute")
    params: Optional[List[Any]] = None


class DBQueryResponse(BaseModel):
    db_type: str
    query: str
    columns: List[str] = Field(default_factory=list)
    rows: List[List[Any]] = Field(default_factory=list)
    row_count: int = 0
    error: Optional[str] = None


class ComparisonRequest(BaseModel):
    db_type: str
    host: str
    port: Optional[int] = None
    database: str
    username: str
    password: str
    query: str
    classified_data: Dict[str, Any]


class MismatchDetail(BaseModel):
    field: str
    expected: Any
    actual: Any


class ComparisonResponse(BaseModel):
    match: bool
    mismatches: List[MismatchDetail] = Field(default_factory=list)
    db_record: Optional[Dict[str, Any]] = None
    classified_data: Dict[str, Any]
