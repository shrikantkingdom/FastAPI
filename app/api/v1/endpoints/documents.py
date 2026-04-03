"""Document processing endpoints – upload, extract, classify."""
import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status

from app.dependencies import get_current_user
from app.schemas.document import (
    ClassificationResult,
    DocumentProcessingResponse,
    ExtractionResult,
)
from app.services.ai_service import AIService, get_ai_service
from app.services.pdf_service import PDFService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_pdf_service() -> PDFService:
    return PDFService()


@router.post(
    "/upload",
    response_model=DocumentProcessingResponse,
    summary="Upload and process a PDF document",
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to process"),
    classify: bool = Form(True, description="Whether to run AI classification"),
    current_user: dict = Depends(get_current_user),
    pdf_service: PDFService = Depends(get_pdf_service),
    ai_service: AIService = Depends(get_ai_service),
):
    """
    Upload a PDF file.  Content is extracted synchronously; AI classification
    can optionally run as a background task.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    content = await file.read()
    extraction: ExtractionResult = await pdf_service.extract_from_bytes(
        content, filename=file.filename
    )

    classification: Optional[ClassificationResult] = None
    if classify:
        classification = await ai_service.classify(extraction.text)

    return DocumentProcessingResponse(
        filename=file.filename,
        extraction=extraction,
        classification=classification,
        status="completed",
    )


@router.post(
    "/extract-path",
    response_model=ExtractionResult,
    summary="Extract content from a PDF at a server-side file path",
)
async def extract_from_path(
    file_path: str = Form(..., description="Absolute path to a PDF file on the server"),
    current_user: dict = Depends(get_current_user),
    pdf_service: PDFService = Depends(get_pdf_service),
):
    """Extract text from a PDF located at the given server-side path."""
    extraction = await pdf_service.extract_from_path(file_path)
    return extraction
