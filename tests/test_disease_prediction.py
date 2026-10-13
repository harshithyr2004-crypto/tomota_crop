# -*- coding: utf-8 -*-
"""
Automated Tests for Stage 2 Tomato Disease Classifier
"""

import os
import sys
import pytest
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.services.disease_service import TomatoDiseaseClassifierService, disease_service_instance
from app.core.config import CLASS_NAMES, VAL_DATASET_DIR

VAL_DIR = VAL_DATASET_DIR

def test_disease_model_loaded():
    """Verify that Stage 2 Disease Model is loaded."""
    assert disease_service_instance.model is not None

def test_disease_diagnosis_output_structure():
    """Verify that diagnosis returns all agronomy advisory fields and health score."""
    sample_cls = "Tomato___healthy"
    sample_dir = VAL_DIR / sample_cls
    assert sample_dir.exists()
    
    img_name = os.listdir(sample_dir)[0]
    img = Image.open(sample_dir / img_name).convert("RGB")

    res = disease_service_instance.diagnose(img, tomato_conf=99.0)
    
    assert "common_name" in res
    assert "confidence" in res
    assert "health_score" in res
    assert 0 <= res["health_score"] <= 100
    assert "symptoms" in res and len(res["symptoms"]) > 0
    assert "organic_treatment" in res and len(res["organic_treatment"]) > 0
    assert "chemical_treatment" in res and len(res["chemical_treatment"]) > 0
    assert "prevention" in res and len(res["prevention"]) > 0
    assert "action_plan" in res
    assert "today" in res["action_plan"]

def test_confidence_explanation_flags_close_alternatives():
    guidance = TomatoDiseaseClassifierService.explain_confidence(
        [
            {"confidence": 48.0},
            {"confidence": 44.0},
        ],
        {"today": "Inspect the newest leaves."},
        "Medium",
        False,
    )

    assert guidance["level"] == "Needs a closer look"
    assert guidance["runner_up_margin"] == 4.0
    assert guidance["is_uncertain"] is True
    assert "rescan" in guidance["next_step"].lower()

def test_confidence_explanation_preserves_action_for_strong_match():
    guidance = TomatoDiseaseClassifierService.explain_confidence(
        [
            {"confidence": 91.0},
            {"confidence": 6.0},
        ],
        {"today": "Remove infected leaves."},
        "Medium",
        False,
    )

    assert guidance["level"] == "Strong match"
    assert guidance["runner_up_margin"] == 85.0
    assert guidance["next_step"] == "Remove infected leaves."
