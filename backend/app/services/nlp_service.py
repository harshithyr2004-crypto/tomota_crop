# -*- coding: utf-8 -*-
"""
NLP utilities for farmer query understanding and intent detection.
This module keeps the app working without external NLP dependencies and
adds lightweight language and intent analysis for the TomatoGuard assistant.
"""

import re
from typing import Dict, Any, Optional, Tuple

from app.data.disease_info import DISEASE_CATALOG


class NLPService:
    """Analyze farmer input for language, intent, and crop disease context."""

    INTENT_KEYWORDS = {
        "prevention": ["prevent", "prevention", "avoid", "protect", "stop"],
        "chemical": ["medicine", "chemical", "spray", "fungicide", "pesticide", "cure", "drug", "treatment", "treat"],
        "organic": ["organic", "natural", "home", "neem", "bio", "baking soda", "manure", "compost"],
        "symptoms": ["symptom", "symptoms", "identify", "sign", "signs", "look like", "appearance", "lesion", "lesions"],
        "action": ["action", "today", "schedule", "timeline", "step", "what to do", "plan"],
        "diagnosis": ["diagnosis", "diagnose", "disease", "what is this", "what is", "what disease", "problem"],
    }

    DISEASE_ALIASES = {
        "Tomato___Spider_mites Two-spotted_spider_mite": ["spider mite", "spider mites", "mites"],
    }

    def normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", (text or "").strip())

    def detect_language(self, text: str) -> str:
        cleaned = self.normalize_text(text)
        if not cleaned:
            return "en"

        if any(ch for ch in cleaned if ord(ch) > 127):
            # Very lightweight detection based on script families.
            if any(ord(ch) in range(0x0900, 0x097F) for ch in cleaned):
                return "hi"
            if any(ord(ch) in range(0x0C00, 0x0C7F) for ch in cleaned):
                return "te"
            if any(ord(ch) in range(0x0B80, 0x0BFF) for ch in cleaned):
                return "kn"
            if any(ord(ch) in range(0x0B00, 0x0B7F) for ch in cleaned):
                return "ta"
            if any(ord(ch) in range(0x0D00, 0x0D7F) for ch in cleaned):
                return "ml"
            if any(ord(ch) in range(0x0980, 0x09FF) for ch in cleaned):
                return "bn"
            if any(ord(ch) in range(0x0A80, 0x0AFF) for ch in cleaned):
                return "gu"
            if any(ord(ch) in range(0x0A00, 0x0A7F) for ch in cleaned):
                return "pa"
            if any(ord(ch) in range(0x0900, 0x0D7F) for ch in cleaned):
                return "hi"

        return "en"

    def detect_intent(self, text: str) -> str:
        query = self.normalize_text(text).lower()
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if re.search(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", query):
                    return intent
        return "general"

    def detect_disease(self, text: str, current_disease: Optional[str] = None) -> Optional[str]:
        query = self.normalize_text(text).lower()
        best_match = None
        best_match_length = 0

        for disease_key, info in DISEASE_CATALOG.items():
            aliases = [
                str(info.get("common_name", "")),
                str(info.get("scientific_name", "")),
                disease_key.removeprefix("Tomato___").replace("_", " "),
                *self.DISEASE_ALIASES.get(disease_key, []),
            ]
            for alias in aliases:
                normalized_alias = self.normalize_text(alias).lower()
                if normalized_alias and re.search(
                    r"(?<!\w)" + re.escape(normalized_alias) + r"(?!\w)", query
                ) and len(normalized_alias) > best_match_length:
                    best_match = disease_key
                    best_match_length = len(normalized_alias)

        if best_match:
            return best_match
        if current_disease and current_disease in DISEASE_CATALOG:
            return current_disease
        return None

    def analyze_question(self, text: str, current_disease: Optional[str] = None) -> Dict[str, Any]:
        cleaned = self.normalize_text(text)
        language = self.detect_language(cleaned)
        intent = self.detect_intent(cleaned)
        disease_key = self.detect_disease(cleaned, current_disease)
        if intent == "general" and disease_key:
            intent = "diagnosis"

        return {
            "text": cleaned,
            "language": language,
            "intent": intent,
            "disease_key": disease_key,
            "cleaned_query": cleaned,
        }


nlp_service_instance = NLPService()
