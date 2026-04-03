"""Tests for DB playground endpoints."""
from unittest.mock import AsyncMock, patch

from app.schemas.db_playground import DBQueryResponse, ComparisonResponse


_DB_PAYLOAD = {
    "db_type": "sqlserver",
    "host": "localhost",
    "port": 1433,
    "database": "testdb",
    "username": "sa",
    "password": "secret",
    "query": "SELECT 1 AS val",
}


def test_query_no_auth(client):
    response = client.post("/api/v1/db/query", json=_DB_PAYLOAD)
    assert response.status_code == 401


def test_query_mocked(client, auth_headers):
    mock_result = DBQueryResponse(
        db_type="sqlserver",
        query="SELECT 1 AS val",
        columns=["val"],
        rows=[[1]],
        row_count=1,
    )
    with patch(
        "app.api.v1.endpoints.db_playground.DBService.run_query",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = client.post(
            "/api/v1/db/query", json=_DB_PAYLOAD, headers=auth_headers
        )
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 1
    assert data["columns"] == ["val"]


def test_compare_mocked(client, auth_headers):
    mock_result = ComparisonResponse(
        match=True,
        mismatches=[],
        db_record={"amount": "100"},
        classified_data={"amount": "100"},
    )
    payload = {**_DB_PAYLOAD, "classified_data": {"amount": "100"}}
    with patch(
        "app.api.v1.endpoints.db_playground.DBService.compare",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = client.post(
            "/api/v1/db/compare", json=payload, headers=auth_headers
        )
    assert response.status_code == 200
    data = response.json()
    assert data["match"] is True


def test_test_connection_mocked(client, auth_headers):
    conn_payload = {
        "db_type": "sqlserver",
        "host": "localhost",
        "port": 1433,
        "database": "testdb",
        "username": "sa",
        "password": "secret",
    }
    with patch(
        "app.api.v1.endpoints.db_playground.DBService.test_connection",
        new_callable=AsyncMock,
        return_value=True,
    ):
        response = client.post(
            "/api/v1/db/test-connection", json=conn_payload, headers=auth_headers
        )
    assert response.status_code == 200
    assert response.json()["status"] == "connected"
