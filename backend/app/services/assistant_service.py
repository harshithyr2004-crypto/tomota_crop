# -*- coding: utf-8 -*-
"""
"Ask TomatoGuard" Contextual AI Agronomy Assistant
Provides accurate, grounded guidance based on the detected plant pathology.
"""

from typing import Dict, Any, Optional

from app.data.disease_info import DISEASE_CATALOG
from app.services.genai_service import genai_service_instance
from app.services.nlp_service import nlp_service_instance


class TomatoGuardAssistantService:
    @staticmethod
    def answer_query(query: str, current_disease: Optional[str] = None) -> Dict[str, Any]:
        q_lower = (query or "").lower()

        analysis = nlp_service_instance.analyze_question(q_lower, current_disease)
        intent = analysis.get("intent", "general")
        use_disease_context = analysis.get("disease_explicit") or intent not in {"general", "pest"}
        disease_key = analysis.get("disease_key") if use_disease_context else None
        disease_info = DISEASE_CATALOG.get(disease_key) if disease_key else None
        common_name = disease_info.get("common_name") if disease_info else "General tomato care"

        # Preserve the legacy rule-based response as a fallback.
        if disease_info and any(w in q_lower for w in ["prevent", "avoid", "protect", "stop", "prevention"]):
            resp = f"🛡️ Prevention Protocol for {common_name}:\n"
            for p in disease_info.get("prevention", []):
                resp += f"• {p}\n"
            resp += "\nTip: Consistent drip irrigation and crop rotation are the strongest barriers against disease."
        elif disease_info and any(w in q_lower for w in ["medicine", "chemical", "spray", "fungicide", "pesticide", "cure", "drug"]):
            resp = f"💊 Recommended Control for {common_name}:\n"
            for c in disease_info.get("chemical_treatment", []):
                resp += f"• {c}\n"
            resp += "\n⚠️ Important: Always follow product label instructions and verify local agricultural authority regulations."
        elif disease_info and any(w in q_lower for w in ["organic", "natural", "home", "neem", "bio", "baking soda"]):
            resp = f"🌿 Organic & Bio-control Remedies for {common_name}:\n"
            for o in disease_info.get("organic_treatment", []):
                resp += f"• {o}\n"
            resp += "\nOrganic approaches work best when applied early in the morning and at initial symptom onset."
        elif disease_info and any(w in q_lower for w in ["symptom", "identify", "sign", "look like", "spot", "yellow"]):
            resp = f"🔍 Typical Symptoms of {common_name}:\n"
            for s in disease_info.get("symptoms", []):
                resp += f"• {s}\n"
            resp += f"\nPathogen Type: {disease_info.get('pathogen_type', 'N/A')} ({disease_info.get('scientific_name', '')})"
        elif disease_info and any(w in q_lower for w in ["action", "today", "schedule", "timeline", "step"]):
            plan = disease_info.get("action_plan", {})
            resp = f"📋 Farmer Action Plan for {common_name}:\n"
            resp += f"• Today: {plan.get('today', 'Inspect affected plants.')}\n"
            resp += f"• Next 3 Days: {plan.get('next_3_days', 'Apply protective spray.')}\n"
            resp += f"• This Week: {plan.get('this_week', 'Improve row aeration.')}\n"
            resp += f"• Long Term: {plan.get('prevention', 'Rotate crops.')}\n"
        elif not disease_info:
            resp = (
                "I can help with tomato growing, watering, soil, fertilizer, pests, diseases, and harvest. "
                "Please include the crop stage or describe the issue so I can give specific guidance."
            )
        else:
            resp = (
                f"🌾 Regarding {common_name} ({disease_info.get('pathogen_type', 'Plant Health')}):\n"
                f"{disease_info.get('symptoms', ['Inspect the leaves for disease symptoms.'])[0]}\n\n"
                f"Recommended first step: {disease_info.get('action_plan', {}).get('today', 'Prune damaged leaves.')}\n\n"
                f"You can ask me specifically about symptoms, organic remedies, chemical sprays, or prevention steps."
            )

        # Add GenAI-powered response on top of the grounded advice.
        genai_response = genai_service_instance.generate_response(
            query=query,
            disease_info=disease_info,
            intent=intent,
            language=analysis.get("language", "en"),
        )

        final_response = genai_response if genai_response else resp

        return {
            "query": query,
            "context_disease": common_name,
            "response": final_response,
            "intent": intent,
            "language": analysis.get("language", "en"),
            "nlp_insights": {
                "disease_key": disease_key,
                "analysis": analysis,
            },
        }


assistant_service_instance = TomatoGuardAssistantService()
