import io
import os
from PIL import Image
import numpy as np

from app.core.config import CLASS_NAMES
from app.data.disease_info import DISEASE_CATALOG
from app.services.disease_service import disease_service_instance
from app.utils.image_processing import load_image_from_bytes

class TomatoClassifier:
    def __init__(self):
        self.service = disease_service_instance
        self.model = self.service.model

    def predict(self, image_bytes: bytes) -> dict:
        pil_img = load_image_from_bytes(image_bytes)
        diag = self.service.diagnose(pil_img)
        
        info = DISEASE_CATALOG.get(diag["raw_class"], {})
        
        return {
            "prediction": {
                "raw_class": diag["raw_class"],
                "common_name": diag["common_name"],
                "confidence": diag["confidence"],
                "is_healthy": diag["is_healthy"],
                "severity": diag["severity"],
                "pathogen": diag.get("pathogen_type", ""),
                "symptoms": " ".join(diag["symptoms"]) if isinstance(diag["symptoms"], list) else str(diag["symptoms"]),
                "organic_treatment": " ".join(diag["organic_treatment"]) if isinstance(diag["organic_treatment"], list) else str(diag["organic_treatment"]),
                "chemical_treatment": " ".join(diag["chemical_treatment"]) if isinstance(diag["chemical_treatment"], list) else str(diag["chemical_treatment"]),
                "prevention": " ".join(diag["prevention"]) if isinstance(diag["prevention"], list) else str(diag["prevention"])
            },
            "top_predictions": diag.get("top_predictions", []),
            "all_predictions": diag.get("all_predictions", [])
        }

classifier_instance = TomatoClassifier()
