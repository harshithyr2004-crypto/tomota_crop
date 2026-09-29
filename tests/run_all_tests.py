# -*- coding: utf-8 -*-
"""
Standalone Automated Test Runner for TomatoGuard AI
"""

import os
import sys
import io
from pathlib import Path
from PIL import Image

# Add paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from app.services.binary_service import binary_service_instance
from app.services.disease_service import disease_service_instance
from app.services.quality_service import quality_service_instance
from app.services.translation_service import translation_service_instance
from app.services.assistant_service import assistant_service_instance

NON_TOMATO_VAL_DIR = BASE_DIR / "ml" / "datasets" / "tomato_binary" / "val" / "not_tomato"
TOMATO_VAL_DIR = BASE_DIR / "ml" / "datasets" / "tomato_binary" / "val" / "tomato_leaf"

def run_tests():
    print("=" * 70)
    print("             TOMATOGUARD AI - AUTOMATED TEST SUITE             ")
    print("=" * 70)

    passed = 0
    total = 0

    def assert_test(name, condition, extra_info=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name} {extra_info}")
        else:
            print(f"  [FAIL] {name} {extra_info}")

    # Test 1: Stage 1 Binary Gate Loaded
    assert_test(
        "Stage 1 Binary Gate Model Loaded",
        binary_service_instance.model is not None,
        f"(Threshold: {binary_service_instance.threshold})"
    )

    # Test 2: Stage 2 Disease Model Loaded
    assert_test(
        "Stage 2 Disease Classifier Model Loaded",
        disease_service_instance.model is not None
    )

    # Test 3: Non-Tomato Zero-Tolerance Rejection Suite
    non_files = [f for f in os.listdir(NON_TOMATO_VAL_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:20]
    rejections = 0
    for f in non_files:
        img = Image.open(NON_TOMATO_VAL_DIR / f).convert("RGB")
        res = binary_service_instance.verify_tomato(img)
        if not res["is_tomato"]:
            rejections += 1
    assert_test(
        "Non-Tomato Rejection Suite",
        rejections >= 19,
        f"({rejections}/{len(non_files)} rejected, {(rejections/len(non_files))*100:.1f}%)"
    )

    # Test 4: Real Tomato Leaf Acceptance Suite
    tom_files = [f for f in os.listdir(TOMATO_VAL_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:20]
    acceptances = 0
    for f in tom_files:
        img = Image.open(TOMATO_VAL_DIR / f).convert("RGB")
        res = binary_service_instance.verify_tomato(img)
        if res["is_tomato"]:
            acceptances += 1
    assert_test(
        "Tomato Leaf Acceptance Suite",
        acceptances >= 19,
        f"({acceptances}/{len(tom_files)} accepted, {(acceptances/len(tom_files))*100:.1f}%)"
    )

    # Test 5: Image Quality Gate (Pitch-Black Image Rejection)
    black_img = Image.new("RGB", (224, 224), (0, 0, 0))
    q_pass, q_report = quality_service_instance.assess_quality(black_img)
    assert_test(
        "Quality Assessment Gate (Dark image rejected)",
        q_pass is False,
        f"({q_report.get('reason', '')})"
    )

    # Test 6: Multilingual Translation Engine
    hi_trans = translation_service_instance.translate("TomatoGuard AI", "hi")
    kn_trans = translation_service_instance.translate("TomatoGuard AI", "kn")
    assert_test(
        "Multilingual Translation Engine (Hindi & Kannada)",
        hi_trans == "टोमेटोगार्ड एआई" and kn_trans == "ಟೊಮೆಟೊಗಾರ್ಡ್ ಎಐ"
    )

    # Test 7: Contextual AI Assistant
    assist_res = assistant_service_instance.answer_query(
        "How to prevent Early Blight?",
        "Tomato___Early_blight"
    )
    assert_test(
        "Ask TomatoGuard AI Assistant Query",
        "Early Blight" in assist_res["context_disease"] and len(assist_res["response"]) > 30
    )

    # Test 8: Crop Health Score Calculation
    healthy_score = disease_service_instance.calculate_health_score(True, "Tomato___healthy", 95.0, 99.0)
    blight_score = disease_service_instance.calculate_health_score(False, "Tomato___Late_blight", 90.0, 99.0)
    assert_test(
        "Crop Health Score Logic (Healthy >= 80, Blight <= 60)",
        healthy_score >= 80 and blight_score <= 60,
        f"(Healthy: {healthy_score}/100, Late Blight: {blight_score}/100)"
    )

    print("\n" + "=" * 70)
    print(f"TEST RESULTS: {passed}/{total} PASSED ({(passed/total)*100:.1f}%)")
    print("=" * 70)
    return passed == total

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
