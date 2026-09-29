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
