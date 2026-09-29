import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.data.disease_info import DISEASE_CATALOG
from app.services.assistant_service import assistant_service_instance
from app.services.genai_service import genai_service_instance
from app.services.nlp_service import nlp_service_instance


def test_explicit_disease_overrides_previous_scan_context():
    analysis = nlp_service_instance.analyze_question(
        "How can I prevent Late Blight?",
        current_disease="Tomato___Early_blight",
    )

    assert analysis["disease_key"] == "Tomato___Late_blight"
    assert analysis["intent"] == "prevention"


def test_disease_phrase_does_not_match_by_shared_words():
    analysis = nlp_service_instance.analyze_question(
        "What are symptoms of bacterial spot?",
        current_disease="Tomato___Early_blight",
    )

    assert analysis["disease_key"] == "Tomato___Bacterial_spot"
    assert analysis["intent"] == "symptoms"


def test_assistant_generates_answer_for_explicit_disease(monkeypatch):
    captured = {}

    def fake_generate_response(query, disease_info=None, intent="general", language="en"):
        captured.update(disease_info=disease_info, intent=intent)
        return "Grounded test answer"

    monkeypatch.setattr(genai_service_instance, "generate_response", fake_generate_response)
    result = assistant_service_instance.answer_query(
        "How can I prevent Late Blight?",
        current_disease="Tomato___Early_blight",
    )

    assert captured["disease_info"] is DISEASE_CATALOG["Tomato___Late_blight"]
    assert captured["intent"] == "prevention"
    assert result["context_disease"] == "Late Blight"
    assert result["response"] == "Grounded test answer"