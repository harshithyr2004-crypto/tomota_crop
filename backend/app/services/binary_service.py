# -*- coding: utf-8 -*-
"""
Stage 1: MobileNetV2 Tomato vs Non-Tomato Verification Gate Service
"""

import json
from pathlib import Path
from PIL import Image
import tensorflow as tf
from typing import Dict, Any

from app.core.config import BINARY_MODEL_PATH, BINARY_METADATA_PATH, TOMATO_CONFIDENCE_THRESHOLD
from app.utils.image_processing import preprocess_for_mobilenet

class TomatoBinaryGateService:
    def __init__(self):
        self.model = None
        self.threshold = TOMATO_CONFIDENCE_THRESHOLD
        self._load_model()

    def _load_model(self):
        if BINARY_MODEL_PATH.exists():
            try:
                self.model = tf.keras.models.load_model(str(BINARY_MODEL_PATH))
                print(f"[BinaryGate] Successfully loaded Stage 1 model from {BINARY_MODEL_PATH}")
            except Exception as e:
                print(f"[BinaryGate] Error loading binary model: {e}")
        else:
            print(f"[BinaryGate] Warning: Model file {BINARY_MODEL_PATH} not found.")

        if BINARY_METADATA_PATH.exists():
            try:
                with open(BINARY_METADATA_PATH, "r") as f:
                    meta = json.load(f)
                    self.threshold = meta.get("confidence_threshold", TOMATO_CONFIDENCE_THRESHOLD)
            except Exception as e:
                print(f"[BinaryGate] Note loading metadata: {e}")

    def verify_tomato(self, pil_img: Image.Image) -> Dict[str, Any]:
        """
        Runs Stage 1 MobileNetV2 binary prediction.
        Returns is_tomato bool, confidence percentage, and gate decision.
        """
        if self.model is None:
            self._load_model()
            if self.model is None:
                # Fail-safe
                return {
                    "is_tomato": False,
                    "tomato_confidence": 0.0,
                    "threshold_applied": self.threshold,
                    "error": "Binary Gate model unavailable"
                }

        tensor = preprocess_for_mobilenet(pil_img)
        prob = float(self.model.predict(tensor, verbose=0)[0][0])
        conf_pct = round(prob * 100, 2)
        is_tomato = (prob >= self.threshold)

        return {
            "is_tomato": is_tomato,
            "tomato_confidence": conf_pct,
            "threshold_applied": self.threshold,
            "status_message": (
                "Verified Tomato Leaf / Crop" 
                if is_tomato else 
                "This image does not appear to belong to the tomato crop."
            ),
            "suggestion": (
                "Proceeding to plant pathology diagnosis."
                if is_tomato else
                "Please upload or capture a clear image of a tomato leaf."
            )
        }

binary_service_instance = TomatoBinaryGateService()
