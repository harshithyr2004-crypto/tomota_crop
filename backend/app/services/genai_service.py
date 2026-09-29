# -*- coding: utf-8 -*-
"""
GenAI wrapper for the TomatoGuard assistant.
It tries to use an OpenAI-compatible API when an API key is configured,
otherwise it falls back to a grounded local response using the disease catalog.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import request, error

from app.data.disease_info import DISEASE_CATALOG


def _load_env_file() -> None:
    """Load a project .env file if it exists without requiring python-dotenv."""
    project_root = Path(__file__).resolve().parents[3]
    env_path = project_root / ".env"
    if not env_path.exists():
        return

    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
    except Exception:
        pass


class GenAIService:
    def __init__(self):
        _load_env_file()
        self.api_key = (
            os.getenv("OPENAI_API_KEY")
            or os.getenv("GENAI_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )
        self.model = os.getenv("GENAI_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
        self.base_url = (
            os.getenv("OPENAI_BASE_URL")
            or os.getenv("GENAI_BASE_URL")
            or "https://api.openai.com/v1"
        )
        self.provider = (os.getenv("GENAI_PROVIDER") or "openai").lower()

    def _fallback_response(self, query: str, disease_info: Dict[str, Any], intent: str, language: str) -> str:
        common_name = disease_info.get("common_name", "Tomato crop")
        response = [
            f"🌾 For {common_name}, the most relevant guidance is:",
        ]

        if intent == "prevention":
            response.append("Use good sanitation, remove infected leaves, improve air circulation, and avoid overhead watering.")
            response.extend(f"• {item}" for item in disease_info.get("prevention", [])[:3])
        elif intent == "chemical":
            response.append("Apply a registered treatment according to label instructions and local agricultural guidance.")
            response.extend(f"• {item}" for item in disease_info.get("chemical_treatment", [])[:3])
        elif intent == "organic":
            response.append("Begin with sanitation and biological control measures, then use neem or appropriate organic sprays early.")
            response.extend(f"• {item}" for item in disease_info.get("organic_treatment", [])[:3])
        elif intent == "symptoms":
            response.append("Look for the following signs on tomato foliage:")
            response.extend(f"• {item}" for item in disease_info.get("symptoms", [])[:4])
        elif intent == "action":
            plan = disease_info.get("action_plan", {})
            response.append(f"Today: {plan.get('today', 'Inspect plants and isolate affected leaves.')}")
            response.append(f"Next 3 days: {plan.get('next_3_days', 'Apply preventive treatment and monitor spread.')}")
            response.append(f"This week: {plan.get('this_week', 'Improve air flow and maintain crop hygiene.')}")
        else:
            response.append(f"{disease_info.get('symptoms', ['Inspect the leaves for disease symptoms.'])[0]}")
            response.append("For a safe first step, inspect the affected leaves and use good crop hygiene before spraying.")

        if language != "en":
            response.append("\nThis answer is grounded in the detected crop issue and local agronomy guidance.")

        return "\n".join(response)

    def _build_prompt(self, query: str, disease_info: Dict[str, Any], intent: str, language: str) -> str:
        common_name = disease_info.get("common_name", "Tomato crop")
        scientific = disease_info.get("scientific_name", "")
        pathogen = disease_info.get("pathogen_type", "")
        symptoms = "\n".join(f"- {item}" for item in disease_info.get("symptoms", [])[:4])
        organic = "\n".join(f"- {item}" for item in disease_info.get("organic_treatment", [])[:3])
        chemical = "\n".join(f"- {item}" for item in disease_info.get("chemical_treatment", [])[:3])
        prevention = "\n".join(f"- {item}" for item in disease_info.get("prevention", [])[:3])

        return (
            "You are TomatoGuard AI, a helpful agronomy assistant for Indian farmers. "
            "Answer in a clear, practical, and farmer-friendly style. "
            f"Language: {language}. "
            f"Current crop issue: {common_name}. "
            f"Scientific name: {scientific}. "
            f"Pathogen: {pathogen}. "
            f"User question: {query}. "
            f"Intent: {intent}. "
            "Keep the answer concise but actionable. "
            "Do not invent treatments. Do not mention that you are an AI model. "
            "Use local agronomy-safe wording and focus on crop health, prevention, treatment, and action steps.\n\n"
            f"Symptoms:\n{symptoms}\n\n"
            f"Organic options:\n{organic}\n\n"
            f"Chemical options:\n{chemical}\n\n"
            f"Prevention:\n{prevention}\n"
        )

    def _request_openai_compatible(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a practical agricultural assistant helping farmers detect and manage tomato crop diseases."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 350,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url.rstrip('/')}/chat/completions"
        req = request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"].strip()

    def generate_response(self, query: str, disease_info: Optional[Dict[str, Any]] = None, intent: str = "general", language: str = "en") -> str:
        if disease_info is None:
            disease_info = DISEASE_CATALOG.get("Tomato___healthy", {})

        if not self.api_key:
            return self._fallback_response(query, disease_info, intent, language)

        try:
            prompt = self._build_prompt(query, disease_info, intent, language)
            message = self._request_openai_compatible(prompt)
            return message or self._fallback_response(query, disease_info, intent, language)
        except (error.HTTPError, error.URLError, KeyError, ValueError, TimeoutError) as exc:
            return self._fallback_response(query, disease_info, intent, language) + f"\n\nNote: External GenAI is unavailable right now, so local guidance is being shown. ({exc})"


genai_service_instance = GenAIService()
