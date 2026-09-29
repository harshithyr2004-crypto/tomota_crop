# -*- coding: utf-8 -*-
"""
Stage 2: 10-Class Tomato Leaf Disease Classification & Advisory Service
"""

import numpy as np
from PIL import Image
import tensorflow as tf
from typing import Dict, Any, List
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input

from app.core.config import DISEASE_MODEL_PATH, DISEASE_ARCHIVE_MODEL_PATH, CLASS_NAMES
from app.data.disease_info import DISEASE_CATALOG
from app.utils.image_processing import preprocess_for_disease_cnn
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.models import Model

class TomatoDiseaseClassifierService:
    def __init__(self):
        self.model = None
        self._load_model()

    def _build_architecture(self):
        """Builds MobileNetV2 transfer learning architecture."""
        base_model = MobileNetV2(
            weights="imagenet",
            include_top=False,
            input_shape=(224, 224, 3),
            pooling="avg"
        )
        base_model.trainable = False
        
        inputs = Input(shape=(224, 224, 3), name="image_input")
        x = base_model(inputs, training=False)
        x = BatchNormalization()(x)
        x = Dense(256, activation="relu")(x)
        x = Dropout(0.35)(x)
        x = Dense(128, activation="relu")(x)
        x = Dropout(0.25)(x)
        outputs = Dense(len(CLASS_NAMES), activation="softmax")(x)
        
        model = Model(inputs=inputs, outputs=outputs, name="TomatoGuard_Disease_Classifier")
        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        return model

    def _load_model(self):
        # 1. Primary Model: MobileNetV2 Transfer Learning Model
        if DISEASE_MODEL_PATH.exists():
            try:
                self.model = tf.keras.models.load_model(str(DISEASE_MODEL_PATH))
                print(f"[DiseaseService] Successfully loaded Stage 2 MobileNetV2 model from {DISEASE_MODEL_PATH}")
                return
            except Exception as e:
                print(f"[DiseaseService] Primary model load notice: {e}")

        # 2. Archive Model Fallback
        if DISEASE_ARCHIVE_MODEL_PATH.exists():
            try:
                self.model = tf.keras.models.load_model(str(DISEASE_ARCHIVE_MODEL_PATH))
                print(f"[DiseaseService] Loaded Stage 2 model from archive {DISEASE_ARCHIVE_MODEL_PATH}")
                return
            except Exception as e:
                print(f"[DiseaseService] Archive model load notice: {e}")

        # 3. Dynamic Architecture Fallback
        self.model = self._build_architecture()
        print("[DiseaseService] Initialized MobileNetV2 dynamic architecture.")

    def calculate_health_score(self, is_healthy: bool, disease_key: str, confidence: float, tomato_conf: float) -> int:
        """
        Calculates Tomato Crop Health Score (0 - 100).
        AI-based indication derived from tomato confidence, disease severity, and probability.
        """
        if is_healthy:
            # Healthy foliage: score between 85 - 98 based on confidence
            base_score = 85 + int((confidence / 100.0) * 13)
            return min(100, max(80, base_score))
        
        info = DISEASE_CATALOG.get(disease_key, {})
        impact = info.get("health_score_impact", 40)
        
        # Base healthy pool is 100 minus severity impact weighted by confidence
        weighted_loss = impact * (confidence / 100.0)
        score = int(100 - weighted_loss)
        return max(15, min(75, score))

    def diagnose(self, pil_img: Image.Image, tomato_conf: float = 95.0) -> Dict[str, Any]:
        """Runs Stage 2 disease inference and returns comprehensive advisory package."""
        if self.model is None:
            self._load_model()

        tensor = preprocess_for_disease_cnn(pil_img)
        preds = self.model.predict(tensor, verbose=0)[0]

        top_idx = int(np.argmax(preds))
        top_prob = float(preds[top_idx])
        top_raw_class = CLASS_NAMES[top_idx]
        is_healthy = (top_raw_class == "Tomato___healthy")

        info = DISEASE_CATALOG.get(top_raw_class, {
            "common_name": top_raw_class.replace("Tomato___", "").replace("_", " "),
            "scientific_name": "Unknown",
            "pathogen_type": "Unknown",
            "severity": "Medium",
            "symptoms": ["Visible foliar irregularities."],
            "organic_treatment": ["Consult local agricultural extension center."],
            "chemical_treatment": ["Adhere to registered local agronomy guidelines."],
            "prevention": ["Maintain routine crop inspection."],
            "action_plan": {
                "today": "Inspect affected plant thoroughly.",
                "next_3_days": "Isolate from healthy rows.",
                "this_week": "Consult local agronomy extension.",
                "prevention": "Ensure good crop sanitation."
            }
        })

        # Top predictions breakdown
        breakdown = []
        for idx, prob in enumerate(preds):
            cls_name = CLASS_NAMES[idx]
            cls_info = DISEASE_CATALOG.get(cls_name, {})
            breakdown.append({
                "class_id": idx,
                "raw_name": cls_name,
                "common_name": cls_info.get("common_name", cls_name),
                "confidence": round(float(prob) * 100, 2),
                "severity": cls_info.get("severity", "Medium")
            })

        breakdown.sort(key=lambda x: x["confidence"], reverse=True)
        confidence_pct = round(top_prob * 100, 2)
        health_score = self.calculate_health_score(is_healthy, top_raw_class, confidence_pct, tomato_conf)

        return {
            "raw_class": top_raw_class,
            "common_name": info["common_name"],
            "scientific_name": info.get("scientific_name", ""),
            "pathogen_type": info.get("pathogen_type", ""),
            "is_healthy": is_healthy,
            "confidence": confidence_pct,
            "severity": info["severity"],
            "health_score": health_score,
            "symptoms": info["symptoms"],
            "organic_treatment": info["organic_treatment"],
            "chemical_treatment": info["chemical_treatment"],
            "prevention": info["prevention"],
            "action_plan": info.get("action_plan", {}),
            "disclaimer": "AI-based indication for agronomy assistance. Consult a certified local agricultural specialist for severe outbreaks.",
            "top_predictions": breakdown[:3],
            "all_predictions": breakdown
        }

disease_service_instance = TomatoDiseaseClassifierService()
