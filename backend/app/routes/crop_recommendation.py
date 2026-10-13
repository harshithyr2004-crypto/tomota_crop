# -*- coding: utf-8 -*-
"""
AgroVision AI - Crop Recommendation API Endpoints
Endpoints for ML Crop Prediction, Agricultural Insights, Dataset Stats, and Contact inquiries.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.services.crop_recommendation_service import crop_service_instance

router = APIRouter()


class CropPredictionRequest(BaseModel):
    N: float = Field(..., ge=0.0, le=200.0, description="Nitrogen content in soil (kg/ha)")
    P: float = Field(..., ge=0.0, le=200.0, description="Phosphorus content in soil (kg/ha)")
    K: float = Field(..., ge=0.0, le=300.0, description="Potassium content in soil (kg/ha)")
    temperature: float = Field(..., ge=0.0, le=60.0, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity in percentage")
    ph: float = Field(..., ge=0.0, le=14.0, description="Soil pH value (0-14)")
    rainfall: float = Field(..., ge=0.0, le=500.0, description="Rainfall in millimeters")


class ContactFormRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=120)
    subject: str = Field(..., min_length=2, max_length=150)
    message: str = Field(..., min_length=5, max_length=2000)


@router.post("/crop/predict")
def predict_crop(req: CropPredictionRequest):
    """
    ML Prediction Endpoint:
    Accepts 7 soil and atmospheric features, returns recommended crop with probabilities and agronomic guidance.
    """
    try:
        return crop_service_instance.predict_crop(
            n=req.N,
            p=req.P,
            k=req.K,
            temperature=req.temperature,
            humidity=req.humidity,
            ph=req.ph,
            rainfall=req.rainfall
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(exc)}")


@router.get("/crop/stats")
def get_crop_stats():
    """Returns verified dataset KPIs, best model accuracy, and feature importances."""
    return crop_service_instance.get_stats()


@router.get("/crop/samples")
def get_sample_crops():
    """Returns curated representative benchmark samples from the dataset for testing."""
    return {"samples": crop_service_instance.get_samples()}


@router.get("/crop/insights")
def get_crop_insights():
    """Returns per-crop statistical profiles and agronomic requirements."""
    return crop_service_instance.get_insights()


@router.get("/crop/model-metrics")
def get_model_metrics():
    """Returns detailed machine learning evaluation dashboard data (confusion matrix, comparison, metrics)."""
    return crop_service_instance.get_model_metrics()


@router.post("/contact")
def submit_contact(req: ContactFormRequest):
    """Receives contact inquiries and confirms receipt."""
    return {
        "success": True,
        "message": f"Thank you, {req.name}. Your inquiry regarding '{req.subject}' has been received by our agricultural advisory team.",
        "inquiry": {
            "name": req.name,
            "email": req.email,
            "subject": req.subject
        }
    }
