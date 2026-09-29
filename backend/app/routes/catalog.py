# -*- coding: utf-8 -*-
"""
Catalog, Samples, and System Health API Routes
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import CLASS_NAMES, VAL_DATASET_DIR
from app.data.disease_info import DISEASE_CATALOG
from app.services.binary_service import binary_service_instance
from app.services.disease_service import disease_service_instance

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "system": "TomatoGuard AI - Production Diagnostic Engine",
        "stage1_gate_loaded": binary_service_instance.model is not None,
        "stage2_disease_loaded": disease_service_instance.model is not None,
        "supported_classes": len(CLASS_NAMES),
        "gate_threshold": binary_service_instance.threshold
    }

@router.get("/classes")
def list_classes():
    results = []
    for idx, cls_name in enumerate(CLASS_NAMES):
        info = DISEASE_CATALOG.get(cls_name, {})
        results.append({
            "id": idx,
            "raw_name": cls_name,
            "common_name": info.get("common_name", cls_name),
            "scientific_name": info.get("scientific_name", ""),
            "severity": info.get("severity", "Medium"),
            "pathogen_type": info.get("pathogen_type", ""),
            "symptoms_preview": info.get("symptoms", [""])[0]
        })
    return {"total": len(results), "classes": results}

@router.get("/samples")
def get_sample_images():
    """Returns sample test images available from the validation dataset."""
    samples = []
    if VAL_DATASET_DIR.exists():
        for cls_name in sorted(os.listdir(VAL_DATASET_DIR)):
            cls_dir = VAL_DATASET_DIR / cls_name
            if cls_dir.is_dir():
                images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if images:
                    chosen = images[0]
                    info = DISEASE_CATALOG.get(cls_name, {})
                    samples.append({
                        "class_name": cls_name,
                        "common_name": info.get("common_name", cls_name),
                        "file_name": chosen,
                        "image_url": f"/api/sample-image/{cls_name}"
                    })
    return {"samples": samples}

@router.get("/sample-image/{class_name}")
def serve_sample_image(class_name: str):
    """Serves a sample image from the validation set."""
    if class_name not in CLASS_NAMES:
        raise HTTPException(status_code=404, detail="Class not found")
    
    cls_dir = VAL_DATASET_DIR / class_name
    if not cls_dir.exists():
        raise HTTPException(status_code=404, detail="Sample dataset folder not found")
    
    images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        raise HTTPException(status_code=404, detail="No images found for this class")
    
    return FileResponse(cls_dir / images[0], media_type="image/jpeg")
