# -*- coding: utf-8 -*-
"""
Stage 1: MobileNetV2 Transfer Learning for Tomato vs Non-Tomato Binary Classification Gate
"""

import os
import sys
import json
import argparse
import numpy as np
import tensorflow as tf
from pathlib import Path
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, Input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

BASE_DIR = Path(r"D:\tomato_crop\tomato-ai-system")
DATASET_DIR = BASE_DIR / "ml" / "datasets" / "tomato_binary"
SAVED_MODELS_DIR = BASE_DIR / "ml" / "saved_models"

def build_binary_model(input_shape=(224, 224, 3)):
    # 1. Load pretrained MobileNetV2 without top classifier
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze base model initially
    base_model.trainable = False

    # 2. Add custom classification head
    inputs = Input(shape=input_shape)
    x = preprocess_input(inputs) # Standard MobileNetV2 [-1, 1] normalization
    x = base_model(x, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.3)(x)
    outputs = Dense(1, activation="sigmoid", name="tomato_probability")(x)

    model = Model(inputs, outputs, name="TomatoGuard_Binary_Gate")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
    )
    return model, base_model

def main():
    parser = argparse.ArgumentParser(description="Train MobileNetV2 Binary Gate")
    parser.add_argument("--epochs", type=int, default=5, help="Epochs for initial head training")
    parser.add_argument("--fine_tune_epochs", type=int, default=3, help="Epochs for fine-tuning")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    args = parser.parse_args()

    SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    train_dir = DATASET_DIR / "train"
    val_dir = DATASET_DIR / "val"

    print("=" * 65)
    print("   STAGE 1: MOBILENETV2 TOMATO VERIFICATION GATE TRAINING   ")
    print("=" * 65)
    print(f"Train Path: {train_dir}")
    print(f"Val Path  : {val_dir}")
    print("=" * 65)

    # 1. Data Generators with Augmentation
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    val_datagen = ImageDataGenerator()

    train_generator = train_datagen.flow_from_directory(
        str(train_dir),
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode="binary",
        shuffle=True
    )

    val_generator = val_datagen.flow_from_directory(
        str(val_dir),
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode="binary",
        shuffle=False
    )

    class_indices = train_generator.class_indices
    print(f"\nClass Indices Mapping: {class_indices}")

    # 2. Build Model
    print("\n[1/3] Constructing MobileNetV2 Transfer Learning Architecture...")
    model, base_model = build_binary_model()
    model.summary()

    # 3. Phase 1 Training (Feature Extraction)
    print(f"\n[2/3] Training Classification Head for {args.epochs} epochs...")
    history_head = model.fit(
        train_generator,
        epochs=args.epochs,
        validation_data=val_generator,
        verbose=1
    )

    # 4. Phase 2 Fine-Tuning
    if args.fine_tune_epochs > 0:
        print(f"\n[3/3] Fine-tuning Top 30 layers of MobileNetV2 for {args.fine_tune_epochs} epochs...")
        base_model.trainable = True
        # Fine-tune only the last 30 layers
        for layer in base_model.layers[:-30]:
            layer.trainable = False

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss="binary_crossentropy",
            metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
        )

        history_finetune = model.fit(
            train_generator,
            epochs=args.fine_tune_epochs,
            validation_data=val_generator,
            verbose=1
        )

    # 5. Save Model & Metadata
    model_save_path = SAVED_MODELS_DIR / "tomato_binary.keras"
    metadata_save_path = SAVED_MODELS_DIR / "tomato_binary_class_names.json"

    model.save(str(model_save_path))
    print(f"\n Successfully saved binary gate model to: {model_save_path}")

    metadata = {
        "model_name": "TomatoGuard_Binary_Gate",
        "architecture": "MobileNetV2",
        "input_shape": [224, 224, 3],
        "class_indices": class_indices,
        "tomato_class_index": class_indices.get("tomato_leaf", 1),
        "confidence_threshold": 0.75
    }
    with open(metadata_save_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f" Successfully saved class metadata to: {metadata_save_path}")

    # Final Evaluation
    print("\n" + "=" * 65)
    print("              FINAL VALIDATION SET EVALUATION              ")
    print("=" * 65)
    eval_results = model.evaluate(val_generator, verbose=0)
    for metric_name, val in zip(model.metrics_names, eval_results):
        print(f"  {metric_name:<12}: {val:.4f}")
    print("=" * 65)
    print(" STAGE 1 BINARY GATE TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == '__main__':
    main()
