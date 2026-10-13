# -*- coding: utf-8 -*-
"""
Stage 2: 10-Class Tomato Leaf Disease Classification & Advisory Service
LiteRT version for Vercel deployment.
"""

import numpy as np
import threading
from PIL import Image
from typing import Dict, Any

from ai_edge_litert.interpreter import Interpreter

from app.core.config import DISEASE_MODEL_PATH, CLASS_NAMES
from app.data.disease_info import DISEASE_CATALOG
from app.utils.image_processing import preprocess_for_disease_cnn


class TomatoDiseaseClassifierService:
    def __init__(self):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self._inference_lock = threading.Lock()
        self._load_model()

    @property
    def model(self):
        return self.interpreter

    def _load_model(self):
        with self._inference_lock:
            if self.interpreter is not None:
                return

            if DISEASE_MODEL_PATH.exists():
                try:
                    interpreter = Interpreter(
                        model_path=str(DISEASE_MODEL_PATH)
                    )
                    interpreter.allocate_tensors()

                    self.interpreter = interpreter
                    self.input_details = interpreter.get_input_details()
                    self.output_details = interpreter.get_output_details()

                    print(
                        f"[DiseaseService] Successfully loaded Stage 2 "
                        f"LiteRT model from {DISEASE_MODEL_PATH}"
                    )

                except Exception as e:
                    print(f"[DiseaseService] Error loading LiteRT model: {e}")
                    self.interpreter = None

            else:
                print(
                    f"[DiseaseService] Warning: Model file "
                    f"{DISEASE_MODEL_PATH} not found."
                )

    def calculate_health_score(
        self,
        is_healthy: bool,
        disease_key: str,
        confidence: float,
        tomato_conf: float
    ) -> int:
        """
        Calculates Tomato Crop Health Score (0 - 100).
        AI-based indication derived from tomato confidence,
        disease severity, and probability.
        """
        if is_healthy:
            base_score = 85 + int((confidence / 100.0) * 13)
            return min(100, max(80, base_score))

        info = DISEASE_CATALOG.get(disease_key, {})
        impact = info.get("health_score_impact", 40)

        weighted_loss = impact * (confidence / 100.0)
        score = int(100 - weighted_loss)

        return max(15, min(75, score))

    @staticmethod
    def explain_confidence(
        predictions: list,
        action_plan: Dict[str, Any],
        severity: str,
        is_healthy: bool,
    ) -> Dict[str, Any]:
        """Explain model confidence as a ranking signal, not a probability guarantee."""
        confidence = predictions[0]["confidence"] if predictions else 0.0
        runner_up = predictions[1]["confidence"] if len(predictions) > 1 else 0.0
        margin = round(confidence - runner_up, 2)

        if confidence >= 80 and margin >= 20:
            level = "Strong match"
            summary = "The leading class is clearly ahead in this model result. Confidence is not a guarantee."
            next_step = action_plan.get("today", "Inspect the plant and follow the recommended care plan.")
        elif confidence < 55 or margin < 10:
            level = "Needs a closer look"
            summary = "The model is uncertain or the leading classes are close; do not rely on this result alone."
            next_step = "Check the symptoms against the guidance and rescan a clear leaf in even natural light."
        else:
            level = "Possible match"
            summary = "This is the leading model result, but other classes remain plausible."
            next_step = action_plan.get("today", "Inspect the plant and compare the visible symptoms.")

        if not is_healthy and severity in {"High", "Critical"}:
            next_step = (
                "Inspect affected plants promptly and seek local agricultural guidance if symptoms are spreading. "
                + next_step
            )

        return {
            "level": level,
            "summary": summary,
            "next_step": next_step,
            "runner_up_margin": margin,
            "is_uncertain": level == "Needs a closer look",
        }

    def diagnose(
        self,
        pil_img: Image.Image,
        tomato_conf: float = 95.0
    ) -> Dict[str, Any]:
        """Runs Stage 2 disease inference and returns comprehensive advisory package."""

        if self.interpreter is None:
            self._load_model()

        if self.interpreter is None:
            return {
                "error": "Disease classification model unavailable"
            }

        try:
            tensor = preprocess_for_disease_cnn(pil_img)
            tensor = np.asarray(tensor, dtype=np.float32)

            with self._inference_lock:
                self.interpreter.set_tensor(
                    self.input_details[0]["index"],
                    tensor
                )

                self.interpreter.invoke()

                preds = self.interpreter.get_tensor(
                    self.output_details[0]["index"]
                )[0]

            top_idx = int(np.argmax(preds))
            top_prob = float(preds[top_idx])

            top_raw_class = CLASS_NAMES[top_idx]
            is_healthy = (top_raw_class == "Tomato___healthy")

            info = DISEASE_CATALOG.get(
                top_raw_class,
                {
                    "common_name": top_raw_class
                    .replace("Tomato___", "")
                    .replace("_", " "),
                    "scientific_name": "Unknown",
                    "pathogen_type": "Unknown",
                    "severity": "Medium",
                    "symptoms": [
                        "Visible foliar irregularities."
                    ],
                    "organic_treatment": [
                        "Consult local agricultural extension center."
                    ],
                    "chemical_treatment": [
                        "Adhere to registered local agronomy guidelines."
                    ],
                    "prevention": [
                        "Maintain routine crop inspection."
                    ],
                    "action_plan": {
                        "today": "Inspect affected plant thoroughly.",
                        "next_3_days": "Isolate from healthy rows.",
                        "this_week": "Consult local agronomy extension.",
                        "prevention": "Ensure good crop sanitation."
                    }
                }
            )

            breakdown = []

            for idx, prob in enumerate(preds):
                cls_name = CLASS_NAMES[idx]
                cls_info = DISEASE_CATALOG.get(cls_name, {})

                breakdown.append({
                    "class_id": idx,
                    "raw_name": cls_name,
                    "common_name": cls_info.get(
                        "common_name",
                        cls_name
                    ),
                    "confidence": round(
                        float(prob) * 100,
                        2
                    ),
                    "severity": cls_info.get(
                        "severity",
                        "Medium"
                    )
                })

            breakdown.sort(
                key=lambda x: x["confidence"],
                reverse=True
            )

            confidence_pct = round(top_prob * 100, 2)

            health_score = self.calculate_health_score(
                is_healthy,
                top_raw_class,
                confidence_pct,
                tomato_conf
            )
            confidence_guidance = self.explain_confidence(
                breakdown,
                info.get("action_plan", {}),
                info["severity"],
                is_healthy,
            )

            return {
                "raw_class": top_raw_class,
                "common_name": info["common_name"],
                "scientific_name": info.get(
                    "scientific_name",
                    ""
                ),
                "pathogen_type": info.get(
                    "pathogen_type",
                    ""
                ),
                "is_healthy": is_healthy,
                "confidence": confidence_pct,
                "severity": info["severity"],
                "health_score": health_score,
                "symptoms": info["symptoms"],
                "organic_treatment": info["organic_treatment"],
                "chemical_treatment": info["chemical_treatment"],
                "prevention": info["prevention"],
                "action_plan": info.get(
                    "action_plan",
                    {}
                ),
                "confidence_guidance": confidence_guidance,
                "disclaimer": (
                    "AI-based indication for agronomy assistance. "
                    "Consult a certified local agricultural specialist "
                    "for severe outbreaks."
                ),
                "top_predictions": breakdown[:3],
                "all_predictions": breakdown
            }

        except Exception as e:
            print(f"[DiseaseService] Prediction error: {e}")

            return {
                "error": f"Disease prediction failed: {str(e)}"
            }


disease_service_instance = TomatoDiseaseClassifierService()
