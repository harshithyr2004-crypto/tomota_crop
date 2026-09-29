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

from app.services.disease_service import disease_service_instance
from app.core.config import CLASS_NAMES

VAL_DIR = Path(r"D:\archive\tomato\val")

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
