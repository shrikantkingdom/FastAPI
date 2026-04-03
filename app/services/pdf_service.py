"""PDF processing service – extract text (and OCR for image pages)."""
import io
import logging
import os
from typing import Optional

from app.schemas.document import ExtractionResult

logger = logging.getLogger(__name__)


class PDFService:
    """
    Extracts text from PDFs using pdfplumber for text pages and
    pytesseract (via Pillow) for image-only pages.
    Falls back gracefully when optional dependencies are unavailable.
    """

    async def extract_from_bytes(
        self, data: bytes, filename: str = "document.pdf"
    ) -> ExtractionResult:
        return self._extract(io.BytesIO(data), filename)

    async def extract_from_path(self, file_path: str) -> ExtractionResult:
        from fastapi import HTTPException, status
        from app.config import settings

        # Resolve symlinks and normalise to prevent directory traversal
        resolved = os.path.realpath(os.path.abspath(file_path))

        # Restrict access to explicitly allowed base directories
        allowed = [os.path.realpath(d) for d in settings.ALLOWED_PDF_DIRS]
        if not any(
            os.path.commonpath([resolved, base]) == base
            for base in allowed
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File path is not within an allowed directory",
            )

        if not resolved.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported",
            )

        if not os.path.isfile(resolved):  # lgtm[py/path-injection]
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )

        with open(resolved, "rb") as fh:  # lgtm[py/path-injection]
            return self._extract(fh, os.path.basename(resolved))

    def _extract(self, file_obj, filename: str) -> ExtractionResult:  # noqa: C901
        try:
            import pdfplumber
        except ImportError:
            logger.warning("pdfplumber not installed – returning empty extraction")
            return ExtractionResult(filename=filename, text="[pdfplumber not installed]")

        pages_text: list[str] = []
        images_found = 0
        ocr_pages: list[int] = []
        metadata: dict = {}

        try:
            with pdfplumber.open(file_obj) as pdf:
                metadata = pdf.metadata or {}
                page_count = len(pdf.pages)
                for i, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ""
                    if not text.strip():
                        # Try OCR on image-based page
                        ocr_text = self._ocr_page(page)
                        if ocr_text:
                            text = ocr_text
                            ocr_pages.append(i)
                        images_found += len(page.images)
                    pages_text.append(text)

        except Exception as exc:
            logger.error(f"PDF extraction failed: {exc}", exc_info=True)
            return ExtractionResult(
                filename=filename, text="", metadata={"error": str(exc)}
            )

        return ExtractionResult(
            filename=filename,
            page_count=page_count,
            text="\n\n".join(pages_text),
            images_found=images_found,
            ocr_pages=ocr_pages,
            metadata={k: str(v) for k, v in metadata.items()},
        )

    def _ocr_page(self, page) -> str:
        """Run pytesseract OCR on a single pdfplumber page."""
        try:
            import pytesseract
            from PIL import Image

            img = page.to_image(resolution=300).original
            return pytesseract.image_to_string(img)
        except Exception as exc:
            logger.debug(f"OCR failed for page: {exc}")
            return ""
