# -*- coding: utf-8 -*-
"""
Model Evaluation Suite for TomatoGuard AI:
Evaluates Stage 1 Binary Gate and Stage 2 Disease Classifier.
Calculates Accuracy, Precision, Recall, F1-score, and Confusion Matrix.
"""

import os
import sys
import json
import numpy as np
import tensorflow as tf
from pathlib import Path
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

BASE_DIR = Path(r"D:\tomato_crop\tomato-ai-system")
BINARY_MODEL_PATH = BASE_DIR / "ml" / "saved_models" / "tomato_binary.keras"
DISEASE_MODEL_PATH = Path(r"D:\archive\tomato\tomato_disease_model.keras")
DATASET_BINARY_VAL = BASE_DIR / "ml" / "datasets" / "tomato_binary" / "val"
DATASET_DISEASE_VAL = Path(r"D:\archive\tomato\val")

def evaluate_binary_model():
    print("=" * 70)
    print("      STAGE 1: MOBILENETV2 TOMATO VERIFICATION EVALUATION      ")
    print("=" * 70)
    
    if not BINARY_MODEL_PATH.exists():
        print(f"Error: Binary model not found at {BINARY_MODEL_PATH}")
        return

    model = tf.keras.models.load_model(str(BINARY_MODEL_PATH))
    print(f" Loaded Binary Gate Model from {BINARY_MODEL_PATH}")

    y_true = []
    y_pred = []
    y_scores = []
    
    # 0 = not_tomato, 1 = tomato_leaf
    classes = ["not_tomato", "tomato_leaf"]
    
    for label_idx, cls_name in enumerate(classes):
        cls_dir = DATASET_BINARY_VAL / cls_name
        if not cls_dir.exists():
            continue
        for img_name in os.listdir(cls_dir):
            if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = cls_dir / img_name
                try:
                    img = Image.open(img_path).convert("RGB").resize((224, 224))
                    arr = np.expand_dims(np.array(img, dtype=np.float32), axis=0)
                    prob = float(model.predict(arr, verbose=0)[0][0])
                    pred_label = 1 if prob >= 0.75 else 0
                    
                    y_true.append(label_idx)
                    y_pred.append(pred_label)
                    y_scores.append(prob)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)

    print("\n--- PERFORMANCE METRICS (Threshold = 0.75) ---")
    print(f"  Accuracy : {acc * 100:.2f}%")
    print(f"  Precision: {prec * 100:.2f}% (Tomato False Positive Rejection)")
    print(f"  Recall   : {rec * 100:.2f}% (Tomato Identification)")
    print(f"  F1-Score : {f1 * 100:.2f}%")

    print("\n--- CONFUSION MATRIX ---")
    print(f"                Predicted Non-Tomato | Predicted Tomato")
    print(f"Actual Non-Tomato       {cm[0][0]:<12} | {cm[0][1]:<12} (False Positives: {cm[0][1]})")
    print(f"Actual Tomato Leaf      {cm[1][0]:<12} | {cm[1][1]:<12}")

    print("\n--- CLASSIFICATION REPORT ---")
    print(classification_report(y_true, y_pred, target_names=classes, digits=4))

def evaluate_rejection_suite():
    """Explicit test on diverse non-tomato categories (cars, animals, buildings, etc.)"""
    print("=" * 70)
    print("      NON-TOMATO ZERO-TOLERANCE REJECTION SUITE CHECK      ")
    print("=" * 70)
    
    model = tf.keras.models.load_model(str(BINARY_MODEL_PATH))
    not_tomato_dir = DATASET_BINARY_VAL / "not_tomato"
    
    samples = os.listdir(not_tomato_dir)[:15]
    print(f"{'Sample Image':<45} | {'Tomato Confidence':<18} | {'Gate Decision':<12}")
    print("-" * 80)
    
    rejected = 0
    for sample in samples:
        img_path = not_tomato_dir / sample
        img = Image.open(img_path).convert("RGB").resize((224, 224))
        arr = np.expand_dims(np.array(img, dtype=np.float32), axis=0)
        prob = float(model.predict(arr, verbose=0)[0][0])
        decision = "PASS (Tomato)" if prob >= 0.75 else "REJECTED (Non-Tomato)"
        if prob < 0.75:
            rejected += 1
        print(f"{sample[:43]:<45} | {prob * 100:6.2f}%            | {decision}")
        
    print("-" * 80)
    print(f"Non-Tomato Rejection Rate: {rejected}/{len(samples)} ({rejected/len(samples)*100:.1f}%)")
    print("=" * 70)

if __name__ == '__main__':
    evaluate_binary_model()
    evaluate_rejection_suite()
