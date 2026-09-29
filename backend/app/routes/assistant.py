# -*- coding: utf-8 -*-
"""
"Ask TomatoGuard" AI Assistant Routes
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services.assistant_service import assistant_service_instance

router = APIRouter()

class AssistantQueryRequest(BaseModel):
    query: str
    current_disease: Optional[str] = None

@router.post("/assistant/ask")
def query_assistant(req: AssistantQueryRequest):
    """Answers farmer questions grounded in the detected pathology and agronomy advice."""
    return assistant_service_instance.answer_query(
        query=req.query,
        current_disease=req.current_disease
    )
