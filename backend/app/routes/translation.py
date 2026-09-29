# -*- coding: utf-8 -*-
"""
Translation API Routes
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

from app.services.translation_service import translation_service_instance

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TranslationResponse(BaseModel):
    original_text: str
    target_language: str
    translated_text: str

@router.get("/languages")
def get_languages():
    """Returns list of supported Indian languages."""
    return {"languages": translation_service_instance.get_supported_languages()}

@router.post("/translate", response_model=TranslationResponse)
def translate_text(req: TranslationRequest):
    """Translates UI labels or guidance text to requested farmer language."""
    translated = translation_service_instance.translate(req.text, req.target_language)
    return {
        "original_text": req.text,
        "target_language": req.target_language,
        "translated_text": translated
    }
