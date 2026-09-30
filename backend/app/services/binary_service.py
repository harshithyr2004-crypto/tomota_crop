# -*- coding: utf-8 -*-
"""
Stage 1: MobileNetV2 Tomato vs Non-Tomato Verification Gate Service
LiteRT version for Vercel deployment.
"""

import json
from pathlib import Path
from PIL import Image
import numpy as np
from ai_edge_litert.interpreter import Interpreter
from typing import Dict, Any

from app.core.config import (
    BINARY_MODEL_PATH,
    BINARY_METADATA_PATH,
    TOMATO_CONFIDENCE_THRESHOLD,
)
from app.utils.image_processing import preprocess_for_mobilenet


class TomatoBinaryGateService:
    def __init__(self):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.threshold = TOMATO_CONFIDENCE_THRESHOLD
        self._load_model()

    def _load_model(self):
        if BINARY_MODEL_PATH.exists():
            try:
                self.interpreter = Interpreter(
                    model_path=str(BINARY_MODEL_PATH)
                )
                self.interpreter.allocate_tensors()

                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()

                print(
                    f"[BinaryGate] Successfully loaded Stage 1 LiteRT model "
                    f"from {BINARY_MODEL_PATH}"
                )

            except Exception as e:
                print(f"[BinaryGate] Error loading LiteRT model: {e}")
                self.interpreter = None

        else:
            print(
                f"[BinaryGate] Warning: Model file "
                f"{BINARY_MODEL_PATH} not found."
            )

        if BINARY_METADATA_PATH.exists():
            try:
                with open(BINARY_METADATA_PATH, "r", encoding="utf-8") as f:
                    meta = json.load(f)

                self.threshold = meta.get(
                    "confidence_threshold",
                    TOMATO_CONFIDENCE_THRESHOLD,
                )

            except Exception as e:
                print(f"[BinaryGate] Note loading metadata: {e}")

    def verify_tomato(self, pil_img: Image.Image) -> Dict[str, Any]:
        """
        Runs Stage 1 LiteRT binary prediction.
        Returns is_tomato bool, confidence percentage, and gate decision.
        """

        if self.interpreter is None:
            self._load_model()

            if self.interpreter is None:
                return {
                    "is_tomato": False,
                    "tomato_confidence": 0.0,
                    "threshold_applied": self.threshold,
                    "error": "Binary Gate model unavailable",
                }

        try:
            tensor = preprocess_for_mobilenet(pil_img)

            # Ensure NumPy float32 input.
            tensor = np.asarray(tensor, dtype=np.float32)

            self.interpreter.set_tensor(
                self.input_details[0]["index"],
                tensor,
            )

            self.interpreter.invoke()

            output = self.interpreter.get_tensor(
                self.output_details[0]["index"]
            )

            prob = float(output[0][0])

            conf_pct = round(prob * 100, 2)
            is_tomato = prob >= self.threshold

            return {
                "is_tomato": is_tomato,
                "tomato_confidence": conf_pct,
                "threshold_applied": self.threshold,
                "status_message": (
                    "Verified Tomato Leaf / Crop"
                    if is_tomato
                    else
                    "This image does not appear to belong to the tomato crop."
                ),
                "suggestion": (
                    "Proceeding to plant pathology diagnosis."
                    if is_tomato
                    else
                    "Please upload or capture a clear image of a tomato leaf."
                ),
            }

        except Exception as e:
            print(f"[BinaryGate] Prediction error: {e}")

            return {
                "is_tomato": False,
                "tomato_confidence": 0.0,
                "threshold_applied": self.threshold,
                "error": f"Binary Gate prediction failed: {str(e)}",
            }


binary_service_instance = TomatoBinaryGateService()
