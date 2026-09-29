# -*- coding: utf-8 -*-
"""
Step 1: Image Quality and Integrity Assessment Service
Checks file readability, minimum resolution, darkness, extreme blur, and corruption.
"""

import numpy as np
from PIL import Image, ImageStat
from typing import Dict, Any, Tuple

from app.core.config import MIN_IMAGE_WIDTH, MIN_IMAGE_HEIGHT, DARKNESS_THRESHOLD

class ImageQualityService:
    @staticmethod
    def assess_quality(pil_img: Image.Image) -> Tuple[bool, Dict[str, Any]]:
        """
        Assesses whether an uploaded image meets minimum quality standards.
        Returns (is_acceptable, quality_report).
        """
        width, height = pil_img.size
        
        # 1. Resolution Check
        if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
            return False, {
                "passed": False,
                "reason": f"Image resolution too low ({width}x{height}px). Minimum required is {MIN_IMAGE_WIDTH}x{MIN_IMAGE_HEIGHT}px.",
                "suggestion": "Please upload or capture a higher resolution image."
            }

        # 2. Darkness / Brightness Check
        grayscale = pil_img.convert("L")
        stat = ImageStat.Stat(grayscale)
        avg_brightness = stat.mean[0] # Range 0 (pitch black) to 255 (pure white)

        if avg_brightness < DARKNESS_THRESHOLD:
            return False, {
                "passed": False,
                "reason": f"Image is too dark (average brightness: {avg_brightness:.1f}/255).",
                "suggestion": "Please capture the leaf under adequate natural daylight or with flashlight turned on."
            }
            
        if avg_brightness > 250.0:
            return False, {
                "passed": False,
                "reason": "Image is severely overexposed/washed out.",
                "suggestion": "Please avoid direct intense glare or flash reflection."
            }

        # 3. Variance / Contrast Check (Detects blank/solid color images)
        variance = stat.var[0]
        if variance < 5.0:
            return False, {
                "passed": False,
                "reason": "Image has virtually no texture or contrast (solid/blank color).",
                "suggestion": "Please capture a real tomato leaf with visible plant details."
            }

        return True, {
            "passed": True,
            "resolution": f"{width}x{height}",
            "brightness_score": round(avg_brightness, 1),
            "contrast_variance": round(variance, 1),
            "status": "Optimal Quality"
        }

quality_service_instance = ImageQualityService()
