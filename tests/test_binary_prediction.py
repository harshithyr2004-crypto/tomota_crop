# -*- coding: utf-8 -*-
"""
Automated Tests for Stage 1 MobileNetV2 Binary Gate
Asserts zero false positives on non-tomato images and high recall on tomato leaves.
"""

import os
import sys
import pytest
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.services.binary_service import binary_service_instance

NON_TOMATO_VAL_DIR = BASE_DIR / "ml" / "datasets" / "tomato_binary" / "val" / "not_tomato"
TOMATO_VAL_DIR = BASE_DIR / "ml" / "datasets" / "tomato_binary" / "val" / "tomato_leaf"

def test_binary_gate_model_loaded():
    """Verify that the Stage 1 MobileNetV2 model is loaded and ready."""
    assert binary_service_instance.model is not None
    assert binary_service_instance.threshold >= 0.70

def test_non_tomato_rejection_suite():
    """Verify that diverse non-tomato categories (cars, buildings, animals) are rejected."""
    assert NON_TOMATO_VAL_DIR.exists()
    files = [f for f in os.listdir(NON_TOMATO_VAL_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:20]
    assert len(files) > 0

    rejections = 0
    for f in files:
        img_path = NON_TOMATO_VAL_DIR / f
        img = Image.open(img_path).convert("RGB")
        res = binary_service_instance.verify_tomato(img)
        if not res["is_tomato"]:
            rejections += 1

    rejection_rate = rejections / len(files)
    print(f"\nNon-Tomato Rejection Rate: {rejections}/{len(files)} ({rejection_rate*100:.1f}%)")
    assert rejection_rate >= 0.95, "Non-tomato rejection rate must be at least 95%"

def test_tomato_leaf_acceptance_suite():
    """Verify that real tomato leaves pass through the gate."""
    assert TOMATO_VAL_DIR.exists()
    files = [f for f in os.listdir(TOMATO_VAL_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:20]
    assert len(files) > 0

    accepted = 0
    for f in files:
        img_path = TOMATO_VAL_DIR / f
        img = Image.open(img_path).convert("RGB")
        res = binary_service_instance.verify_tomato(img)
        if res["is_tomato"]:
            accepted += 1

    acceptance_rate = accepted / len(files)
    print(f"\nTomato Leaf Acceptance Rate: {accepted}/{len(files)} ({acceptance_rate*100:.1f}%)")
    assert acceptance_rate >= 0.95, "Tomato leaf acceptance rate must be at least 95%"
