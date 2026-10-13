# -*- coding: utf-8 -*-
"""
Automated Integration Tests for FastAPI API Endpoints
"""

import io
import os
import sys
import pytest
from pathlib import Path
from PIL import Image
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.main import app
from app.core.config import MAX_FILE_SIZE_MB
from app.services.binary_service import binary_service_instance
from app.services.disease_service import disease_service_instance
from app.services.genai_service import genai_service_instance
from app.services.quality_service import quality_service_instance

client = TestClient(app)

def test_api_health():
    """Test /api/health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["stage1_gate_loaded"] is True
    assert data["stage2_disease_loaded"] is True
    assert data["supported_classes"] == 10

def test_api_classes():
    """Test /api/classes catalog endpoint."""
    response = client.get("/api/classes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 10
    assert len(data["classes"]) == 10

def test_api_translate():
    """Test /api/translate multilingual endpoint."""
    response = client.post("/api/translate", json={
        "text": "TomatoGuard AI",
        "target_language": "hi"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["translated_text"] == "टोमेटोगार्ड एआई"

def test_api_assistant():
    """Test /api/assistant/ask endpoint."""
    response = client.post("/api/assistant/ask", json={
        "query": "How to prevent Early Blight?",
        "current_disease": "Tomato___Early_blight"
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "Early Blight" in data["context_disease"]

def test_predict_non_tomato_rejection():
    """Test that a non-tomato image (e.g. building/car) is gated with is_tomato=False."""
    non_tomato_dir = BASE_DIR / "ml" / "datasets" / "tomato_binary" / "val" / "not_tomato"
    sample_file = os.listdir(non_tomato_dir)[0]
    
    with open(non_tomato_dir / sample_file, "rb") as f:
        response = client.post("/api/predict", files={"file": (sample_file, f, "image/jpeg")})
        
    assert response.status_code == 200
    data = response.json()
    assert data["is_tomato"] is False
    assert data["tomato_confidence"] < 75.0
    assert "disease" not in data or data["disease"] is None
    assert "⚠️" in data["message"] or "does not appear" in data["message"]

def test_predict_quality_rejection_dark_image():
    """Test that a completely pitch-black image is rejected by Quality Check."""
    black_img = Image.new("RGB", (224, 224), (0, 0, 0))
    buf = io.BytesIO()
    black_img.save(buf, format="JPEG")
    buf.seek(0)
    
    response = client.post("/api/predict", files={"file": ("dark.jpg", buf, "image/jpeg")})
    assert response.status_code == 200
    data = response.json()
    assert data["is_quality_passed"] is False
    assert "too low" in data["message"] or "dark" in data["quality_report"]["reason"]

def test_predict_rejects_upload_above_size_limit():
    payload = b"x" * (int(MAX_FILE_SIZE_MB * 1024 * 1024) + 1)

    response = client.post(
        "/api/predict",
        files={"file": ("large.jpg", payload, "image/jpeg")},
    )

    assert response.status_code == 413
    assert "upload limit" in response.json()["detail"]

def test_predict_runs_inference_off_event_loop(monkeypatch):
    import asyncio
    import threading

    called_off_event_loop = []

    def accept_quality(_image):
        return True, {"passed": True}

    def reject_as_non_tomato(_image):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            called_off_event_loop.append(threading.get_ident() != threading.main_thread().ident)
        return {
            "is_tomato": False,
            "tomato_confidence": 12.0,
            "threshold_applied": 0.75,
        }

    monkeypatch.setattr(quality_service_instance, "assess_quality", accept_quality)
    monkeypatch.setattr(binary_service_instance, "verify_tomato", reject_as_non_tomato)

    image = Image.new("RGB", (224, 224), (30, 120, 30))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = client.post(
        "/api/predict",
        files={"file": ("leaf.jpg", buffer, "image/jpeg")},
    )

    assert response.status_code == 200
    assert response.json()["is_tomato"] is False
    assert called_off_event_loop == [True]

def test_predict_reports_unavailable_gate_as_service_error(monkeypatch):
    monkeypatch.setattr(
        quality_service_instance,
        "assess_quality",
        lambda _image: (True, {"passed": True}),
    )
    monkeypatch.setattr(
        binary_service_instance,
        "verify_tomato",
        lambda _image: {"error": "model unavailable"},
    )

    image = Image.new("RGB", (224, 224), (30, 120, 30))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = client.post(
        "/api/predict",
        files={"file": ("leaf.jpg", buffer, "image/jpeg")},
    )

    assert response.status_code == 503
    assert "temporarily unavailable" in response.json()["detail"]

def test_predict_includes_explainable_confidence_and_action_guidance(monkeypatch):
    monkeypatch.setattr(
        quality_service_instance,
        "assess_quality",
        lambda _image: (True, {"passed": True}),
    )
    monkeypatch.setattr(
        binary_service_instance,
        "verify_tomato",
        lambda _image: {
            "is_tomato": True,
            "tomato_confidence": 96.0,
            "threshold_applied": 0.75,
        },
    )
    monkeypatch.setattr(
        disease_service_instance,
        "diagnose",
        lambda _image, tomato_conf: {
            "raw_class": "Tomato___Early_blight",
            "common_name": "Early Blight",
            "scientific_name": "Alternaria solani",
            "pathogen_type": "Fungal",
            "is_healthy": False,
            "confidence": 49.0,
            "severity": "Medium",
            "health_score": 61,
            "symptoms": ["Dark lesions on older leaves."],
            "organic_treatment": ["Remove infected leaves."],
            "chemical_treatment": ["Use registered products per label."],
            "prevention": ["Avoid wet foliage."],
            "action_plan": {"today": "Inspect lower leaves."},
            "top_predictions": [
                {"common_name": "Early Blight", "confidence": 49.0},
                {"common_name": "Septoria Leaf Spot", "confidence": 44.0},
            ],
            "confidence_guidance": {
                "level": "Needs a closer look",
                "summary": "The leading classes are close.",
                "next_step": "Compare symptoms and rescan in even light.",
                "runner_up_margin": 5.0,
                "is_uncertain": True,
            },
        },
    )
    monkeypatch.setattr(
        genai_service_instance,
        "generate_response",
        lambda **_kwargs: "Inspect the lower leaves and compare visible signs.",
    )

    image = Image.new("RGB", (224, 224), (30, 120, 30))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = client.post(
        "/api/predict",
        files={"file": ("leaf.jpg", buffer, "image/jpeg")},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["confidence_guidance"]["level"] == "Needs a closer look"
    assert result["confidence_guidance"]["runner_up_margin"] == 5.0
