"""Tests for document processing endpoints."""
import io
from unittest.mock import AsyncMock, patch, MagicMock

from app.schemas.document import ClassificationResult, ExtractionResult


def _make_pdf_bytes() -> bytes:
    """Create a minimal valid-looking byte string for testing."""
    return b"%PDF-1.4 mock pdf content"


def test_upload_no_auth(client):
    """Uploading without auth should return 401."""
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test.pdf", _make_pdf_bytes(), "application/pdf")},
        data={"classify": "true"},
    )
    assert response.status_code == 401


def test_upload_non_pdf(client, auth_headers):
    """Uploading a non-PDF file should return 400."""
    with (
        patch(
            "app.api.v1.endpoints.documents.PDFService.extract_from_bytes",
            new_callable=AsyncMock,
        ) as mock_extract,
    ):
        mock_extract.return_value = ExtractionResult(filename="test.txt", text="hello")
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.txt", b"hello", "text/plain")},
            data={"classify": "false"},
            headers=auth_headers,
        )
    assert response.status_code == 400


def test_upload_pdf_mock(client, auth_headers):
    """A PDF upload with mocked services should return 202."""
    mock_extraction = ExtractionResult(
        filename="sample.pdf",
        page_count=2,
        text="Invoice total: $100",
    )
    mock_classification = ClassificationResult(
        category="invoice",
        confidence=0.9,
        summary="Invoice document",
        tags=["invoice"],
    )

    with (
        patch(
            "app.api.v1.endpoints.documents.PDFService.extract_from_bytes",
            new_callable=AsyncMock,
            return_value=mock_extraction,
        ),
        patch(
            "app.api.v1.endpoints.documents.AIService.classify",
            new_callable=AsyncMock,
            return_value=mock_classification,
        ),
    ):
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("sample.pdf", _make_pdf_bytes(), "application/pdf")},
            data={"classify": "true"},
            headers=auth_headers,
        )

    assert response.status_code == 202
    data = response.json()
    assert data["filename"] == "sample.pdf"
    assert data["status"] == "completed"
