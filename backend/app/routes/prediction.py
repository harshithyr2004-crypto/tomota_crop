# -*- coding: utf-8 -*-
"""
Two-Stage AI Diagnostic Prediction API Route
Step 1: Quality Check -> Step 2: Tomato Gate -> Step 3: Disease CNN -> Step 4: Farmer Advisory
Supports Full Multilingual Localization for 10 Indian Languages
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from starlette.concurrency import run_in_threadpool
from typing import Any, Dict, Optional

from app.core.config import MAX_FILE_SIZE_MB
from app.utils.image_processing import load_image_from_bytes
from app.services.quality_service import quality_service_instance
from app.services.binary_service import binary_service_instance
from app.services.disease_service import disease_service_instance
from app.services.translation_service import translation_service_instance
from app.services.genai_service import genai_service_instance
from app.data.disease_info import DISEASE_CATALOG

router = APIRouter()


def _process_prediction(contents: bytes, lang: str) -> Dict[str, Any]:
    try:
        pil_img = load_image_from_bytes(contents)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Corrupted or unreadable image file. Please provide a valid image.",
        ) from exc

    quality_passed, quality_report = quality_service_instance.assess_quality(pil_img)
    if not quality_passed:
        raw_msg = "⚠️ Image quality is too low."
        raw_sug = quality_report.get("suggestion", "Please capture a clear, well-lit image of the tomato leaf.")
        return {
            "is_quality_passed": False,
            "quality_report": quality_report,
            "is_tomato": False,
            "tomato_confidence": 0.0,
            "message": translation_service_instance.translate(raw_msg, lang),
            "suggestion": translation_service_instance.translate(raw_sug, lang)
        }

    gate_result = binary_service_instance.verify_tomato(pil_img)
    if gate_result.get("error"):
        raise HTTPException(
            status_code=503,
            detail="Tomato verification is temporarily unavailable.",
        )

    is_tomato = gate_result["is_tomato"]
    tomato_confidence = gate_result["tomato_confidence"]
    if not is_tomato:
        raw_msg = "⚠️ This image does not appear to belong to the tomato crop."
        raw_sug = "Please upload or capture a clear tomato leaf image. Disease diagnosis requires a verified tomato crop leaf."
        return {
            "is_quality_passed": True,
            "quality_report": quality_report,
            "is_tomato": False,
            "tomato_confidence": tomato_confidence,
            "threshold_applied": gate_result["threshold_applied"],
            "message": translation_service_instance.translate(raw_msg, lang),
            "suggestion": translation_service_instance.translate(raw_sug, lang)
        }

    disease_result = disease_service_instance.diagnose(pil_img, tomato_conf=tomato_confidence)
    if disease_result.get("error"):
        raise HTTPException(
            status_code=503,
            detail="Disease diagnosis is temporarily unavailable.",
        )

    disease_info = DISEASE_CATALOG.get(disease_result.get("raw_class"), disease_result)
    ai_summary = genai_service_instance.generate_response(
        query=(
            f"Give a concise farmer-friendly summary for {disease_result.get('common_name', 'this tomato disease')} "
            "with the likely symptoms, immediate action, and prevention advice."
        ),
        disease_info=disease_info,
        intent="diagnosis",
        language=lang,
    )

    disease_name = disease_result["common_name"]
    symptoms = disease_result["symptoms"]
    organic_treatment = disease_result["organic_treatment"]
    chemical_treatment = disease_result["chemical_treatment"]
    prevention = disease_result["prevention"]
    action_plan = disease_result["action_plan"]
    gate_status = "✅ Tomato Crop Verified"

    if lang != "en":
        gate_status = translation_service_instance.translate(gate_status, lang)
        disease_name = translation_service_instance.translate(disease_name, lang)
        symptoms = [translation_service_instance.translate(s, lang) for s in symptoms]
        organic_treatment = [translation_service_instance.translate(o, lang) for o in organic_treatment]
        chemical_treatment = [translation_service_instance.translate(c, lang) for c in chemical_treatment]
        prevention = [translation_service_instance.translate(p, lang) for p in prevention]
        action_plan = {
            "today": translation_service_instance.translate(action_plan.get("today", ""), lang),
            "next_3_days": translation_service_instance.translate(action_plan.get("next_3_days", ""), lang),
            "this_week": translation_service_instance.translate(action_plan.get("this_week", ""), lang)
        }

    return {
        "is_quality_passed": True,
        "quality_report": quality_report,
        "is_tomato": True,
        "tomato_confidence": tomato_confidence,
        "threshold_applied": gate_result["threshold_applied"],
        "gate_status": gate_status,
        "disease": disease_name,
        "raw_class": disease_result["raw_class"],
        "scientific_name": disease_result["scientific_name"],
        "pathogen_type": disease_result["pathogen_type"],
        "confidence": disease_result["confidence"],
        "is_healthy": disease_result["is_healthy"],
        "severity": disease_result["severity"],
        "health_score": disease_result["health_score"],
        "symptoms": symptoms,
        "organic_treatment": organic_treatment,
        "chemical_treatment": chemical_treatment,
        "prevention": prevention,
        "action_plan": action_plan,
        "top_predictions": disease_result.get("top_predictions", []),
        "confidence_guidance": disease_result.get("confidence_guidance", {}),
        "ai_summary": ai_summary
    }


@router.post("/predict")
async def diagnose_crop_image(
    file: UploadFile = File(...),
    target_language: Optional[str] = Form("en")
):
    """
    Two-Stage Prediction Endpoint:
    1. Validates Image Quality (Resolution, Darkness, Corruption).
    2. Stage 1 Binary Gate (MobileNetV2: Tomato vs Non-Tomato / Other Crops).
    3. Stage 2 Disease Classifier (Runs ONLY IF Tomato Authenticity is Verified).
    4. Automatically translates output to selected Indian language.
    """
    lang = (target_language or "en").strip().lower()

    # 1. File Type Validation
    if file.filename:
        ext = file.filename.split(".")[-1].lower()
        if ext not in ["jpg", "jpeg", "png", "webp"]:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload JPG, JPEG, PNG, or WEBP.")

    max_upload_bytes = int(MAX_FILE_SIZE_MB * 1024 * 1024)
    try:
        contents = await file.read(max_upload_bytes + 1)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Failed to read uploaded file.") from exc

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(contents) > max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Image exceeds the {MAX_FILE_SIZE_MB:g} MB upload limit.",
        )

    return await run_in_threadpool(_process_prediction, contents, lang)
