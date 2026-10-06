# -*- coding: utf-8 -*-
"""
GenAI wrapper for the TomatoGuard assistant.
It tries to use an OpenAI-compatible API when an API key is configured,
otherwise it falls back to a grounded local response using the disease catalog.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import request, error

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

    def _general_fallback_response(self, query: str) -> str:
        question = query.lower().strip()

        def mentions(*terms: str) -> bool:
            return any(re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", question) for term in terms)

        if re.fullmatch(r"(hi|hello|hey|good morning|good afternoon|good evening)[!. ]*", question):
            return "Hello! Ask me about tomato diseases, pests, fertilizer, watering, or other crop-care questions."
        if mentions("fertilizer", "fertiliser", "nutrient", "feeding", "manure"):
            return (
                "For tomato fertilizer, start with a soil test and mix mature compost into the bed before planting. "
                "Use a balanced fertilizer according to its label or local extension advice, then avoid excess nitrogen, "
                "which can produce lots of leaves but fewer fruits."
            )
        if mentions("water", "watering", "irrigation", "irrigate", "dry"):
            return (
                "Keep the root zone evenly moist rather than alternating between very dry and waterlogged soil. "
                "Water at soil level, preferably in the morning, and adjust frequency for rainfall, heat, and soil type."
            )
        if mentions("soil", "compost", "pH", "drainage"):
            return (
                "Tomatoes grow best in fertile, well-drained soil with organic matter. "
                "Use a soil test to guide pH and nutrient adjustments, and avoid planting where water stands after rain."
            )
        if mentions("spacing", "space", "apart", "distance", "row"):
            return (
                "Space tomato plants so mature foliage gets good airflow and sunlight. "
                "The right distance depends on the variety and whether plants are staked; follow the seed packet or local extension guidance."
            )
        if mentions("sun", "sunlight", "shade", "light"):
            return "Choose a sunny site with at least 6 hours of direct light daily; more sun generally supports better flowering and fruiting."
        if mentions("prune", "pruning", "stake", "cage", "support", "sucker"):
            return (
                "Support tomato plants with clean stakes or cages before they become heavy. "
                "Remove leaves touching the soil, keep airflow through the plant, and avoid heavy pruning unless the variety and growing system call for it."
            )
        if mentions("harvest", "ripe", "pick", "picking"):
            return (
                "Harvest tomatoes when they reach the mature color and size for their variety and yield slightly to gentle pressure. "
                "Use clean scissors or support the stem while picking to avoid breaking branches."
            )
        if mentions("seed", "seedling", "transplant", "sowing", "germinate", "planting"):
            return (
                "Use healthy seeds or seedlings suited to your local season. Harden seedlings gradually before transplanting, "
                "plant after frost risk has passed, and water them in well."
            )
        if mentions("whitefly", "whiteflies", "white fly", "white flies"):
            return (
                "For whiteflies on tomatoes, inspect leaf undersides and use yellow sticky cards to monitor adults. "
                "Remove heavily infested leaves and nearby weeds, and protect beneficial insects. If treatment is needed, "
                "use only a locally registered product labeled for whiteflies on tomatoes and follow its label. "
                "Whiteflies can spread tomato yellow leaf curl virus, so monitor plants for leaf curling and yellowing."
            )
        if mentions("pest", "pests", "insect", "insects", "aphid", "aphids", "caterpillar", "caterpillars", "bug", "bugs"):
            return (
                "Inspect both sides of leaves and new growth to identify the pest before treating. "
                "Remove small infestations by hand or water where practical; use only locally registered products and follow the label."
            )

        return (
            "I can help with tomato growing, watering, soil, fertilizer, pests, diseases, and harvest. "
            "Please add the crop stage, location, or symptoms so I can give a specific, reliable answer."
        )

    def _fallback_response(self, query: str, disease_info: Optional[Dict[str, Any]], intent: str, language: str) -> str:
        if not disease_info:
            return self._general_fallback_response(query)

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

    def _build_prompt(self, query: str, disease_info: Optional[Dict[str, Any]], intent: str, language: str) -> str:
        crop_context = "No disease has been identified; answer the general tomato-growing question directly."
        reference_material = "No disease-specific reference material is applicable."
        if disease_info:
            crop_context = (
                f"Detected issue: {disease_info.get('common_name', 'Tomato crop')}. "
                f"Scientific name: {disease_info.get('scientific_name', '')}. "
                f"Pathogen: {disease_info.get('pathogen_type', '')}."
            )
            sections = {
                "Symptoms": disease_info.get("symptoms", [])[:4],
                "Organic options": disease_info.get("organic_treatment", [])[:3],
                "Chemical options": disease_info.get("chemical_treatment", [])[:3],
                "Prevention": disease_info.get("prevention", [])[:3],
            }
            reference_material = "\n\n".join(
                f"{title}:\n" + "\n".join(f"- {item}" for item in items)
                for title, items in sections.items() if items
            )

        return (
            "You are TomatoGuard AI, a helpful agronomy assistant for Indian farmers. "
            "Answer the user's actual question directly in a clear, practical, farmer-friendly style. "
            f"Language: {language}. "
            f"{crop_context} "
            f"User question: {query}\n"
            f"Intent: {intent}. "
            "Keep the answer concise but actionable. If the question is outside tomato agriculture, say so briefly and still answer if you know. "
            "Do not invent treatments. Do not mention that you are an AI model. "
            "Use agronomy-safe wording and do not force disease advice onto general questions.\n\n"
            f"Reference material, when relevant:\n{reference_material}\n"
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
        if not self.api_key:
            return self._fallback_response(query, disease_info, intent, language)

        try:
            prompt = self._build_prompt(query, disease_info, intent, language)
            message = self._request_openai_compatible(prompt)
            return message or self._fallback_response(query, disease_info, intent, language)
        except (error.HTTPError, error.URLError, KeyError, ValueError, TimeoutError) as exc:
            return self._fallback_response(query, disease_info, intent, language) + f"\n\nNote: External GenAI is unavailable right now, so local guidance is being shown. ({exc})"


genai_service_instance = GenAIService()
