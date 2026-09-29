import os
from pathlib import Path

# Base Paths (Points to D:\tomato_crop\tomato-ai-system)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PROJECT_ROOT = BASE_DIR
ML_DIR = BASE_DIR / "ml"
SAVED_MODELS_DIR = ML_DIR / "saved_models"

# Stage 1: MobileNetV2 Binary Gate Model
BINARY_MODEL_PATH = SAVED_MODELS_DIR / "tomato_binary.keras"
BINARY_METADATA_PATH = SAVED_MODELS_DIR / "tomato_binary_class_names.json"
TOMATO_CONFIDENCE_THRESHOLD = 0.75  # Configurable gate threshold (75%)

# Stage 2: Disease Classifier Model (MobileNetV2 Transfer Learning Engine)
DISEASE_MODEL_PATH = SAVED_MODELS_DIR / "tomato_disease_mobilenet.keras"
DISEASE_ARCHIVE_MODEL_PATH = Path(r"D:\archive\tomato\tomato_disease_model.keras")
DISEASE_WEIGHTS_PATH = Path(r"D:\archive\tomato\keras_potato_trained_model_weights.weights.h5")

# Datasets
VAL_DATASET_DIR = Path(r"D:\archive\tomato\val")
TRAIN_DATASET_DIR = Path(r"D:\archive\tomato\train")

# Static Frontend
STATIC_FRONTEND_DIR = BASE_DIR / "frontend"

# Quality Check Config
MIN_IMAGE_WIDTH = 64
MIN_IMAGE_HEIGHT = 64
MAX_FILE_SIZE_MB = 15.0
DARKNESS_THRESHOLD = 15.0  # Average brightness below this is considered too dark
BLUR_LAPLACIAN_THRESHOLD = 12.0 # Variance of Laplacian for blur detection

# 10 Supported Tomato Categories
CLASS_NAMES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]
