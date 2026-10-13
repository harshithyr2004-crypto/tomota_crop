# -*- coding: utf-8 -*-
"""
GenAI Service for TomatoGuard AI Assistant.
Supports:
1. Google Gemini API (Direct Gemini REST or OpenAI-compatible) - Free tier supported
2. OpenAI API (GPT-4o / GPT-4o-mini)
3. Groq Cloud (Ultra-Fast Llama-3.3)
4. Custom OpenAI-compatible endpoints
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib import request, error

# Default endpoints and models
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_env_file() -> None:
    """Load a project .env file if it exists."""
    env_path = get_project_root() / ".env"
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
            os.environ[key] = value
    except Exception:
        pass


def save_env_values(values: Dict[str, str]) -> None:
    """Persist key-value pairs into the project .env file."""
    env_path = get_project_root() / ".env"
    existing_lines = []
    if env_path.exists():
        try:
            existing_lines = env_path.read_text(encoding="utf-8").splitlines()
        except Exception:
            existing_lines = []

    existing_keys = set()
    new_lines = []
    for line in existing_lines:
        trimmed = line.strip()
        if trimmed and not trimmed.startswith("#") and "=" in trimmed:
            k = trimmed.split("=", 1)[0].strip()
            if k in values:
                new_lines.append(f"{k}={values[k]}")
                existing_keys.add(k)
                continue
        new_lines.append(line)

    for k, v in values.items():
        if k not in existing_keys:
            new_lines.append(f"{k}={v}")

    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


class GenAIService:
    def __init__(self):
        self.reload_config()

    def reload_config(self) -> None:
        """Reload configuration from environment and .env."""
        load_env_file()

        # Check explicit keys
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        self.openai_key = os.getenv("OPENAI_API_KEY") or ""
        self.groq_key = os.getenv("GROQ_API_KEY") or ""
        self.generic_key = os.getenv("GENAI_API_KEY") or ""

        # Determine active provider
        env_provider = (os.getenv("GENAI_PROVIDER") or "").lower()
        if env_provider:
            self.provider = env_provider
        elif self.gemini_key:
            self.provider = "gemini"
        elif self.groq_key:
            self.provider = "groq"
        elif self.openai_key:
            self.provider = "openai"
        elif self.generic_key:
            self.provider = "openai"
        else:
            self.provider = "gemini"  # Default recommended provider

        # Determine effective active key
        if self.provider == "gemini":
            self.api_key = self.gemini_key or self.generic_key
            self.model = os.getenv("GENAI_MODEL") or os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL
            self.base_url = os.getenv("GEMINI_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta"
        elif self.provider == "groq":
            self.api_key = self.groq_key or self.generic_key
            self.model = os.getenv("GENAI_MODEL") or os.getenv("GROQ_MODEL") or DEFAULT_GROQ_MODEL
            self.base_url = os.getenv("GROQ_BASE_URL") or "https://api.groq.com/openai/v1"
        elif self.provider == "openai":
            self.api_key = self.openai_key or self.generic_key
            self.model = os.getenv("GENAI_MODEL") or os.getenv("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL
            self.base_url = os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        elif self.provider == "custom":
            self.api_key = self.generic_key or self.openai_key or self.gemini_key
            self.model = os.getenv("GENAI_MODEL") or "default"
            self.base_url = os.getenv("GENAI_BASE_URL") or "https://api.openai.com/v1"
        else:
            self.provider = "gemini"
            self.api_key = ""
            self.model = DEFAULT_GEMINI_MODEL
            self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def get_status(self) -> Dict[str, Any]:
        """Return safe view of current GenAI configuration."""
        masked_key = ""
        if self.api_key:
            if len(self.api_key) > 8:
                masked_key = f"{self.api_key[:4]}...{self.api_key[-4:]}"
            else:
                masked_key = "***"

        return {
            "provider": self.provider,
            "model": self.model,
            "has_custom_key": bool(self.api_key),
            "masked_key": masked_key,
            "base_url": self.base_url,
            "ready": bool(self.api_key),
        }

    def update_config(self, provider: str, api_key: str = "", model: str = "", base_url: str = "") -> Tuple[bool, str]:
        """Update provider settings in memory and persist to .env."""
        prov = (provider or "gemini").lower()
        key = (api_key or "").strip()
        mod = (model or "").strip()
        url = (base_url or "").strip()

        env_updates = {
            "GENAI_PROVIDER": prov,
        }

        if prov == "gemini":
            mod = mod or DEFAULT_GEMINI_MODEL
            env_updates["GEMINI_API_KEY"] = key
            env_updates["GENAI_MODEL"] = mod
            if url:
                env_updates["GEMINI_BASE_URL"] = url
        elif prov == "groq":
            mod = mod or DEFAULT_GROQ_MODEL
            env_updates["GROQ_API_KEY"] = key
            env_updates["GENAI_MODEL"] = mod
            if url:
                env_updates["GROQ_BASE_URL"] = url
        elif prov == "openai":
            mod = mod or DEFAULT_OPENAI_MODEL
            env_updates["OPENAI_API_KEY"] = key
            env_updates["GENAI_MODEL"] = mod
            if url:
                env_updates["OPENAI_BASE_URL"] = url
        elif prov == "custom":
            env_updates["GENAI_API_KEY"] = key
            env_updates["GENAI_MODEL"] = mod or "default"
            env_updates["GENAI_BASE_URL"] = url or "https://api.openai.com/v1"

        try:
            save_env_values(env_updates)
            for k, v in env_updates.items():
                os.environ[k] = v
            self.reload_config()
            return True, f"AI Provider '{prov.upper()}' configured successfully."
        except Exception as e:
            return False, f"Failed to save settings: {e}"

    def _build_prompt(self, query: str, disease_info: Optional[Dict[str, Any]], intent: str, language: str) -> str:
        """Construct prompt suitable for both agricultural and general questions."""
        has_disease = bool(disease_info)
        context_parts = []
        if has_disease:
            common_name = disease_info.get("common_name", "Tomato crop issue")
            scientific = disease_info.get("scientific_name", "")
            pathogen = disease_info.get("pathogen_type", "")
            context_parts.append(f"Current Tomato Pathology Context: {common_name} ({scientific}, Pathogen: {pathogen}).")
            
            symptoms = disease_info.get("symptoms", [])[:3]
            if symptoms:
                context_parts.append("Symptoms: " + "; ".join(symptoms))
            organic = disease_info.get("organic_treatment", [])[:2]
            if organic:
                context_parts.append("Organic Options: " + "; ".join(organic))
            chemical = disease_info.get("chemical_treatment", [])[:2]
            if chemical:
                context_parts.append("Chemical Options: " + "; ".join(chemical))
            prevention = disease_info.get("prevention", [])[:2]
            if prevention:
                context_parts.append("Prevention: " + "; ".join(prevention))

        diag_context = "\n".join(context_parts) if context_parts else "No specific disease is selected."

        return (
            "You are TomatoGuard AI Advisor, an intelligent agricultural expert and versatile general assistant.\n"
            "Instructions:\n"
            "1. CROP / AGRI QUESTIONS: Provide accurate, practical, structured agronomy advice (symptoms, organic/chemical controls, spray dosage, irrigation, prevention). Include safety tips.\n"
            "2. OUTSIDE / GENERAL QUESTIONS: If the user asks ANY general knowledge, geography, science, math, history, or outside question (e.g., 'What is the capital of India?', 'How do solar panels work?', 'Explain photosynthesis'), ALWAYS ANSWER DIRECTLY, ACCURATELY, AND FULLY. Do not refuse or complain that it is outside agriculture.\n"
            "3. LANGUAGE: Match the user's language (English, Kannada, Hindi, Telugu, Tamil, Marathi, Bengali, etc.). If asked in Kannada, answer in clear Kannada.\n"
            "4. STYLE: Use clean bullet points, bold text, and short paragraphs for easy reading.\n\n"
            f"[Diagnosis Context if applicable]:\n{diag_context}\n\n"
            f"[User Query]: {query}\n"
            f"[Intent Detected]: {intent}\n"
            f"[Detected Language]: {language}\n"
            "Please answer below:"
        )

    def _call_gemini_native(self, prompt: str, key: str, model: str) -> str:
        """Call Google Gemini REST API directly."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 1000
            }
        }
        req = request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()
            raise ValueError("No response generated by Gemini.")

    def _call_openai_compatible(self, prompt: str, base_url: str, key: str, model: str) -> str:
        """Call any OpenAI-compatible API endpoint (OpenAI, Groq, OpenRouter)."""
        clean_base = base_url.rstrip("/")
        if not clean_base.endswith("/chat/completions"):
            endpoint = f"{clean_base}/chat/completions"
        else:
            endpoint = clean_base

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are TomatoGuard AI Advisor, an expert agronomy consultant and versatile assistant. Answer all user questions accurately, politely, and thoroughly."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 900
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "TomatoGuard-AI/2.0"
        }
        if key:
            headers["Authorization"] = f"Bearer {key}"

        req = request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()

    def test_key(self, provider: str, api_key: str, model: str = "") -> Tuple[bool, str]:
        """Test a provider key with a quick test prompt."""
        if not api_key:
            return False, "Please enter an API key to test."

        test_prompt = "Say in 5 words: 'TomatoGuard AI is ready!'"
        try:
            prov = provider.lower()
            if prov == "gemini":
                mod = model or DEFAULT_GEMINI_MODEL
                res = self._call_gemini_native(test_prompt, api_key, mod)
            elif prov == "groq":
                mod = model or DEFAULT_GROQ_MODEL
                res = self._call_openai_compatible(test_prompt, "https://api.groq.com/openai/v1", api_key, mod)
            elif prov == "openai":
                mod = model or DEFAULT_OPENAI_MODEL
                res = self._call_openai_compatible(test_prompt, "https://api.openai.com/v1", api_key, mod)
            else:
                mod = model or "default"
                res = self._call_openai_compatible(test_prompt, self.base_url, api_key, mod)

            return True, f"Connection verified! Response: {res}"
        except error.HTTPError as e:
            try:
                err_data = json.loads(e.read().decode())
                err_msg = err_data.get("error", {}).get("message", str(e))
                return False, f"API Error ({e.code}): {err_msg}"
            except Exception:
                return False, f"HTTP Error {e.code}: {e.reason}"
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"

    def _local_agronomy_fallback(self, query: str, disease_info: Optional[Dict[str, Any]], intent: str) -> str:
        """Offline fallback if internet is unreachable or no key is set."""
        q_lower = query.lower()
        if disease_info:
            common = disease_info.get("common_name", "Tomato Crop")
            resp = [f"🌾 **{common} Guidance (Offline Catalog):**"]
            if intent in ["chemical", "spray"] and disease_info.get("chemical_treatment"):
                resp.append("\n**Recommended Treatments:**")
                for item in disease_info.get("chemical_treatment", [])[:3]:
                    resp.append(f"• {item}")
            elif intent in ["organic", "bio"] and disease_info.get("organic_treatment"):
                resp.append("\n**Organic & Bio Remedies:**")
                for item in disease_info.get("organic_treatment", [])[:3]:
                    resp.append(f"• {item}")
            else:
                resp.append("\n**Symptoms & Action Plan:**")
                for item in disease_info.get("symptoms", [])[:3]:
                    resp.append(f"• {item}")
                plan = disease_info.get("action_plan", {})
                if plan:
                    resp.append(f"• Immediate Action: {plan.get('today', 'Inspect affected leaves.')}")
            return "\n".join(resp)

        if any(w in q_lower for w in ["about tomato", "tomato crop", "growing tomato", "cultivation", "tell about"]):
            return (
                "🍅 **Tomato (*Solanum lycopersicum*) Cultivation Overview:**\n\n"
                "• **Climate & Temperature:** Warm-season crop requiring 21°C–29°C for optimal growth. Sensitive to frost and extreme heat (>35°C causes flower drop).\n"
                "• **Soil Requirements:** Fertile, well-draining sandy loam with pH 6.0–6.8, enriched with decomposed farmyard manure (FYM).\n"
                "• **Irrigation Strategy:** Regular drip irrigation directly to root zones. Avoid overhead spraying to reduce foliar fungal outbreaks.\n"
                "• **Nutrient Management:** Balanced N-P-K (19:19:19) at early vegetative stage; switch to high Potassium (13:0:45) and Calcium Nitrate during flowering & fruit set.\n"
                "• **Pest & Disease Defense:** Monitor for Whiteflies, Spider Mites, Early Blight, and Late Blight. Use yellow sticky cards and prophylactic copper sprays.\n"
                "• **Harvesting:** Harvest at breaker or pink stage for long transport, or vine-ripe for direct local consumption.\n\n"
                "💡 *Connect your free Gemini API key in **⚙️ AI Settings** to enable unlimited live cloud AI responses for any question!*"
            )

        if any(w in q_lower for w in ["water", "irrigation"]):
            return "💧 **Tomato Watering Guidance:** Water at soil level in early morning. Keep root zone evenly moist and avoid splashing leaves."
        if any(w in q_lower for w in ["fertilizer", "nutrient", "npk"]):
            return "🌱 **Fertilization Guidance:** Use balanced NPK during growth. Increase Potassium & Calcium during flowering and fruit development."
        if any(w in q_lower for w in ["blight", "yellow"]):
            return "🍂 **Yellow Leaves / Blight:** Prune lowest infected leaves. Apply copper bactericide or neem oil. Avoid excess moisture."

        return (
            "🌾 **General Agronomy Advisory:**\n"
            f"You asked: '{query}'.\n\n"
            "To answer any customized or outside knowledge question with live AI, connect your free Google Gemini API key or OpenAI key via **⚙️ AI Settings / Connect Key** above!"
        )

    def _call_free_cloud(self, prompt: str) -> str:
        """Zero-config high-performance free cloud AI (Pollinations OpenAI-Fast)."""
        for model_name in ["openai-fast", "openai"]:
            try:
                return self._call_openai_compatible(
                    prompt=prompt,
                    base_url="https://text.pollinations.ai/openai/chat/completions",
                    key="",
                    model=model_name
                )
            except Exception as e:
                print(f"[TomatoGuard AI] Free cloud model '{model_name}' attempt failed: {e}")
                continue
        raise RuntimeError("Free cloud AI endpoints busy")

    def generate_response(
        self,
        query: str,
        disease_info: Optional[Dict[str, Any]] = None,
        intent: str = "general",
        language: str = "en"
    ) -> str:
        """
        Generate response for ANY question:
        1. If user configured an API key (Gemini, OpenAI, Groq), uses that key.
        2. If key is unset or has an issue, automatically uses Free Cloud AI (answers any question out of the box).
        3. If offline, falls back to local agronomy catalog.
        """
        prompt = self._build_prompt(query, disease_info, intent, language)

        # 1. Custom key provider if configured
        if self.api_key:
            try:
                if self.provider == "gemini":
                    return self._call_gemini_native(prompt, self.api_key, self.model)
                elif self.provider in ["openai", "groq", "custom"]:
                    return self._call_openai_compatible(prompt, self.base_url, self.api_key, self.model)
            except Exception as e:
                print(f"[TomatoGuard AI] Configured provider '{self.provider}' error: {e}. Falling back to Free Cloud AI.")

        # 2. Free Cloud AI (Zero-setup, no key needed, answers ANY outside or crop query)
        try:
            return self._call_free_cloud(prompt)
        except Exception as e:
            print(f"[TomatoGuard AI] Free Cloud AI error: {e}. Falling back to offline guidance.")

        # 3. Local offline fallback
        return self._local_agronomy_fallback(query, disease_info, intent)



genai_service_instance = GenAIService()
