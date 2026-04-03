"""AI service abstraction layer – classify document text."""
import logging
from typing import Optional

from fastapi import Depends

from app.config import settings
from app.schemas.document import ClassificationResult

logger = logging.getLogger(__name__)


class AIService:
    """Abstract base for AI providers."""

    async def classify(self, text: str) -> ClassificationResult:
        raise NotImplementedError


class MockAIService(AIService):
    """Mock provider – returns deterministic results without calling any API."""

    async def classify(self, text: str) -> ClassificationResult:
        logger.debug("MockAIService.classify called")
        category = "general"
        if "invoice" in text.lower():
            category = "invoice"
        elif "contract" in text.lower():
            category = "contract"
        elif "report" in text.lower():
            category = "report"

        return ClassificationResult(
            category=category,
            confidence=0.85,
            summary=f"Document classified as '{category}' by mock AI.",
            tags=[category, "processed"],
            raw_response={"provider": "mock"},
        )


class OpenAIService(AIService):
    """OpenAI-backed classifier (requires OPENAI_API_KEY)."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    async def classify(self, text: str) -> ClassificationResult:
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.api_key)
            snippet = text[:3000]
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a document classifier. Given the text excerpt, "
                            "respond with JSON: {category, confidence, summary, tags}."
                        ),
                    },
                    {"role": "user", "content": snippet},
                ],
                response_format={"type": "json_object"},
            )
            import json

            raw = json.loads(response.choices[0].message.content)
            return ClassificationResult(
                category=raw.get("category", "unknown"),
                confidence=float(raw.get("confidence", 0.5)),
                summary=raw.get("summary", ""),
                tags=raw.get("tags", []),
                raw_response=raw,
            )
        except Exception as exc:
            logger.error(f"OpenAI classification failed: {exc}", exc_info=True)
            return ClassificationResult(
                category="error",
                confidence=0.0,
                summary=str(exc),
            )


def get_ai_service() -> AIService:
    """Dependency factory – returns the configured AI service."""
    if settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
        return OpenAIService(
            api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL
        )
    return MockAIService()
