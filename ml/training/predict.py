# -*- coding: utf-8 -*-
"""
Tomato Crop Disease Prediction / Inference Script
Location: d:/tomato_crop/tomato-ai-system/ml/training/predict.py
"""

import os
import sys
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

CLASS_NAMES = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

def load_trained_model(weights_path=r'D:\archive\tomato\keras_potato_trained_model_weights.weights.h5', model_path=r'D:\archive\tomato\tomato_disease_model.keras'):
    if os.path.exists(model_path):
        try:
            model = tf.keras.models.load_model(model_path)
            print(f" Loaded full model from {model_path}")
            return model
        except Exception as e:
            print(f"Could not load full model: {e}")

    from train import build_model
    model = build_model(input_shape=(128, 128, 3), num_classes=len(CLASS_NAMES))
    if os.path.exists(weights_path):
        model.load_weights(weights_path)
        print(f" Loaded weights from {weights_path}")
    else:
        print(f" Weights file not found: {weights_path}")
    return model

def predict_single_image(model, img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_batch, verbose=0)[0]
    top_idx = int(np.argmax(predictions))
    top_prob = float(predictions[top_idx])
    predicted_class = CLASS_NAMES[top_idx]
    
    return predicted_class, top_prob, predictions

def test_sample_predictions(model, val_dir=r'D:\archive\tomato\val', samples_per_class=1):
    print("\n" + "=" * 90)
    print("                 SAMPLE PREDICTIONS ON VALIDATION DATASET                 ")
    print("=" * 90)
    print(f"{'Actual Class':<40} | {'Predicted Class':<40} | {'Confidence':<10} | Match")
    print("-" * 90)
    
    correct = 0
    total = 0

    for cls in sorted(os.listdir(val_dir)):
        cls_path = os.path.join(val_dir, cls)
        if os.path.isdir(cls_path):
            files = [f for f in os.listdir(cls_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for f in files[:samples_per_class]:
                img_file = os.path.join(cls_path, f)
                pred_cls, conf, _ = predict_single_image(model, img_file)
                is_correct = (cls == pred_cls)
                if is_correct:
                    correct += 1
                total += 1
                match_str = "[MATCH]" if is_correct else "[DIFF]"
                print(f"{cls:<40} | {pred_cls:<40} | {conf*100:6.2f}%   | {match_str}")

    print("-" * 90)
    print(f"Sample Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    print("=" * 90)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict Tomato Disease")
    parser.add_argument('--image', type=str, default=None, help="Path to single image")
    parser.add_argument('--weights', type=str, default=r'D:\archive\tomato\keras_potato_trained_model_weights.weights.h5')
    args = parser.parse_args()

    model = load_trained_model(args.weights)
    if args.image and os.path.exists(args.image):
        pred_cls, conf, _ = predict_single_image(model, args.image)
        print(f"\nResult: {pred_cls} ({conf*100:.2f}% confidence)")
    else:
        test_sample_predictions(model)
