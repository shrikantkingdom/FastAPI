"""Pydantic schemas for document processing."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ExtractionResult(BaseModel):
    filename: str
    page_count: int = 0
    text: str = ""
    images_found: int = 0
    ocr_pages: List[int] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClassificationResult(BaseModel):
    category: str
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str = ""
    tags: List[str] = Field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


class DocumentProcessingResponse(BaseModel):
    filename: str
    status: str
    extraction: ExtractionResult
    classification: Optional[ClassificationResult] = None
