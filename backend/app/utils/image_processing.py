# -*- coding: utf-8 -*-
"""
Image Processing Utilities for TomatoGuard AI
"""

import io
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """Safely loads and converts image bytes to RGB PIL Image."""
    image = Image.open(io.BytesIO(image_bytes))
    return image.convert("RGB")

def preprocess_for_mobilenet(pil_img: Image.Image, target_size=(224, 224)) -> np.ndarray:
    """Preprocesses image for MobileNetV2 Stage 1 Binary Gate (224x224, float32 array)."""
    resized = pil_img.resize(target_size, Image.Resampling.BILINEAR)
    arr = np.array(resized, dtype=np.float32)
    return np.expand_dims(arr, axis=0)

def preprocess_for_disease_cnn(pil_img: Image.Image, target_size=(224, 224)) -> np.ndarray:
    """Preprocesses image for Stage 2 MobileNetV2 Classifier (224x224, normalized float32 array)."""
    resized = pil_img.resize(target_size, Image.Resampling.BILINEAR)
    arr = np.array(resized, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    return preprocess_input(arr)

