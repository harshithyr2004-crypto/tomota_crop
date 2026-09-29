import os
import random
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from app.core.config import CLASS_NAMES, VAL_DATASET_DIR
from app.data.disease_info import DISEASE_CATALOG
from app.services.disease_service import disease_service_instance
from app.utils.image_processing import load_image_from_bytes

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "system": "TomatoGuard AI - Crop Health Diagnostic Engine",
        "model_loaded": disease_service_instance.model is not None,
        "supported_classes": len(CLASS_NAMES)
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
            "severity": info.get("severity", "Medium"),
            "pathogen": info.get("pathogen_type", ""),
            "symptoms": info.get("symptoms", [""])[0] if isinstance(info.get("symptoms"), list) else str(info.get("symptoms", ""))
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
    """Serves a real image from the validation set for quick UI testing."""
    if class_name not in CLASS_NAMES:
        raise HTTPException(status_code=404, detail="Class not found")
    
    cls_dir = VAL_DATASET_DIR / class_name
    if not cls_dir.exists():
        raise HTTPException(status_code=404, detail="Sample dataset folder not found")
    
    images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        raise HTTPException(status_code=404, detail="No images found for this class")
    
    return FileResponse(cls_dir / images[0], media_type="image/jpeg")

@router.post("/predict")
async def diagnose_leaf(file: UploadFile = File(...)):
    """Receives a leaf image, runs diagnosis, and returns pathology report."""
    try:
        contents = await file.read()
        if not contents or len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        pil_img = load_image_from_bytes(contents)
        result = disease_service_instance.diagnose(pil_img)
        result["filename"] = file.filename or "uploaded_leaf.jpg"
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
