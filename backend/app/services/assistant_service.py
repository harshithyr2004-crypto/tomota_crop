# -*- coding: utf-8 -*-
"""
"Ask TomatoGuard" Contextual AI Agronomy Assistant
Provides accurate, grounded guidance based on the detected plant pathology.
"""

from typing import Dict, Any, Optional
from app.data.disease_info import DISEASE_CATALOG

class TomatoGuardAssistantService:
    @staticmethod
    def answer_query(query: str, current_disease: Optional[str] = None) -> Dict[str, Any]:
        q_lower = query.lower()
        
        # 1. Identify context
        disease_info = None
        if current_disease and current_disease in DISEASE_CATALOG:
            disease_info = DISEASE_CATALOG[current_disease]
        else:
            # Try to infer disease from query words
            for key, info in DISEASE_CATALOG.items():
                if info["common_name"].lower() in q_lower:
                    disease_info = info
                    break
        
        if not disease_info:
            disease_info = DISEASE_CATALOG.get("Tomato___healthy")

        # 2. Match question intents
        common_name = disease_info["common_name"]
        
        if any(w in q_lower for w in ["prevent", "avoid", "protect", "stop", "prevention"]):
            resp = f"🛡️ Prevention Protocol for {common_name}:\n"
            for p in disease_info["prevention"]:
                resp += f"• {p}\n"
            resp += "\nTip: Consistent drip irrigation and crop rotation are the strongest barriers against disease."
            
        elif any(w in q_lower for w in ["medicine", "chemical", "spray", "fungicide", "pesticide", "cure", "drug"]):
            resp = f"💊 Recommended Control for {common_name}:\n"
            for c in disease_info["chemical_treatment"]:
                resp += f"• {c}\n"
            resp += "\n⚠️ Important: Always follow product label instructions and verify local agricultural authority regulations."
            
        elif any(w in q_lower for w in ["organic", "natural", "home", "neem", "bio", "baking soda"]):
            resp = f"🌿 Organic & Bio-control Remedies for {common_name}:\n"
            for o in disease_info["organic_treatment"]:
                resp += f"• {o}\n"
            resp += "\nOrganic approaches work best when applied early in the morning and at initial symptom onset."
            
        elif any(w in q_lower for w in ["symptom", "identify", "sign", "look like", "spot", "yellow"]):
            resp = f"🔍 Typical Symptoms of {common_name}:\n"
            for s in disease_info["symptoms"]:
                resp += f"• {s}\n"
            resp += f"\nPathogen Type: {disease_info.get('pathogen_type', 'N/A')} ({disease_info.get('scientific_name', '')})"
            
        elif any(w in q_lower for w in ["action", "today", "schedule", "timeline", "step"]):
            plan = disease_info.get("action_plan", {})
            resp = f"📋 Farmer Action Plan for {common_name}:\n"
            resp += f"• Today: {plan.get('today', 'Inspect affected plants.')}\n"
            resp += f"• Next 3 Days: {plan.get('next_3_days', 'Apply protective spray.')}\n"
            resp += f"• This Week: {plan.get('this_week', 'Improve row aeration.')}\n"
            resp += f"• Long Term: {plan.get('prevention', 'Rotate crops.')}\n"
            
        else:
            resp = (
                f"🌾 Regarding {common_name} ({disease_info.get('pathogen_type', 'Plant Health')}):\n"
                f"{disease_info['symptoms'][0]}\n\n"
                f"Recommended first step: {disease_info.get('action_plan', {}).get('today', 'Prune damaged leaves.')}\n\n"
                f"You can ask me specifically about symptoms, organic remedies, chemical sprays, or prevention steps."
            )

        return {
            "query": query,
            "context_disease": common_name,
            "response": resp
        }

assistant_service_instance = TomatoGuardAssistantService()
