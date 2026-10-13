# -*- coding: utf-8 -*-
"""
"Ask TomatoGuard" AI Assistant Routes
Provides:
- Answering user queries (crop & general knowledge)
- Getting active AI provider & key configuration
- Updating/saving AI provider & key settings
- Testing API keys before saving
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services.assistant_service import assistant_service_instance

router = APIRouter()


class AssistantQueryRequest(BaseModel):
    query: str
    current_disease: Optional[str] = None


class AIConfigRequest(BaseModel):
    provider: str
    api_key: Optional[str] = ""
    model: Optional[str] = ""
    base_url: Optional[str] = ""


class AITestKeyRequest(BaseModel):
    provider: str
    api_key: str
    model: Optional[str] = ""


@router.post("/assistant/ask")
def query_assistant(req: AssistantQueryRequest):
    """Answers farmer questions grounded in the detected pathology and agronomy advice, or any general question."""
    return assistant_service_instance.answer_query(
        query=req.query,
        current_disease=req.current_disease
    )


@router.get("/assistant/config")
def get_ai_config():
    """Retrieve current AI provider, status, and model info."""
    return assistant_service_instance.get_config()


@router.post("/assistant/config")
def update_ai_config(req: AIConfigRequest):
    """Update AI provider and API key in runtime and persist to .env."""
    return assistant_service_instance.update_config(
        provider=req.provider,
        api_key=req.api_key or "",
        model=req.model or "",
        base_url=req.base_url or ""
    )


@router.post("/assistant/test-key")
def test_ai_key(req: AITestKeyRequest):
    """Test connection with given AI provider and API key."""
    return assistant_service_instance.test_key(
        provider=req.provider,
        api_key=req.api_key,
        model=req.model or ""
    )
