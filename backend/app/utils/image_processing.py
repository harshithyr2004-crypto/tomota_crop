# -*- coding: utf-8 -*-
"""
Image Processing Utilities for TomatoGuard AI
"""

import io
import numpy as np
from PIL import Image


def load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    """Safely loads and converts image bytes to RGB PIL Image."""
    image = Image.open(io.BytesIO(image_bytes))
    return image.convert("RGB")


def preprocess_for_mobilenet(
    pil_img: Image.Image,
    target_size=(224, 224)
) -> np.ndarray:
    """Preprocesses image for Stage 1 Binary Gate."""
    resized = pil_img.resize(
        target_size,
        Image.Resampling.BILINEAR
    )

    arr = np.array(
        resized,
        dtype=np.float32
    )

    return np.expand_dims(arr, axis=0)


def preprocess_for_disease_cnn(
    pil_img: Image.Image,
    target_size=(224, 224)
) -> np.ndarray:
    """
    Preprocesses image for Stage 2 MobileNetV2.

    Equivalent to TensorFlow MobileNetV2 preprocess_input:
        x = (x / 127.5) - 1.0
    """

    resized = pil_img.resize(
        target_size,
        Image.Resampling.BILINEAR
    )

    arr = np.array(
        resized,
        dtype=np.float32
    )

    arr = (arr / 127.5) - 1.0

    return np.expand_dims(arr, axis=0)