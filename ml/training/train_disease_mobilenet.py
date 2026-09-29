# -*- coding: utf-8 -*-
"""
High-Accuracy 10-Class Tomato Crop Disease & Health Classification using MobileNetV2 Transfer Learning
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
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, Input, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Suppress verbose TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

BASE_DIR = Path(r"D:\tomato_crop\tomato-ai-system")
ARCHIVE_DIR = Path(r"D:\archive\tomato")
SAVED_MODELS_DIR = BASE_DIR / "ml" / "saved_models"

def build_disease_model(input_shape=(224, 224, 3), num_classes=10):
    # 1. Base Pretrained MobileNetV2
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape
    )
    base_model.trainable = False

    # 2. Architecture with internal preprocessing
    inputs = Input(shape=input_shape)
    x = preprocess_input(inputs)
    x = base_model(x, training=False)
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.35)(x)
    outputs = Dense(num_classes, activation="softmax", name="disease_probability")(x)

    model = Model(inputs, outputs, name="TomatoGuard_Disease_Classifier")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model, base_model

def main():
    parser = argparse.ArgumentParser(description="Train MobileNetV2 10-Class Tomato Disease Classifier")
    parser.add_argument("--epochs", type=int, default=4, help="Epochs for classification head")
    parser.add_argument("--fine_tune_epochs", type=int, default=3, help="Epochs for fine-tuning")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--train_dir", type=str, default=r"D:\archive\tomato\train", help="Train dataset path")
    parser.add_argument("--val_dir", type=str, default=r"D:\archive\tomato\val", help="Val dataset path")
    args = parser.parse_args()

    SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    train_dir = Path(args.train_dir)
    val_dir = Path(args.val_dir)

    print("=" * 70)
    print("  STAGE 2: MOBILENETV2 10-CLASS TOMATO DISEASE & HEALTH CLASSIFIER  ")
    print("=" * 70)
    print(f"Train Dataset: {train_dir}")
    print(f"Val Dataset  : {val_dir}")
    print(f"Batch Size   : {args.batch_size}")
    print("=" * 70)

    # 1. Data Generators with Augmentation
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    val_datagen = ImageDataGenerator()

    train_generator = train_datagen.flow_from_directory(
        str(train_dir),
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=True
    )

    val_generator = val_datagen.flow_from_directory(
        str(val_dir),
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=False
    )

    class_indices = train_generator.class_indices
    print("\nClass Mapping:")
    sorted_classes = sorted(class_indices.items(), key=lambda x: x[1])
    for cls_name, idx in sorted_classes:
        print(f"  [{idx}] {cls_name}")

    # 2. Build Model
    print("\n[1/3] Building MobileNetV2 Transfer Learning Architecture...")
    model, base_model = build_disease_model(input_shape=(224, 224, 3), num_classes=len(class_indices))
    model.summary()

    callbacks = [
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=1, min_lr=1e-6, verbose=1),
        EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True, verbose=1)
    ]

    # 3. Phase 1: Train Custom Top Layers
    print(f"\n[2/3] Phase 1: Training Classification Head ({args.epochs} epochs)...")
    history_phase1 = model.fit(
        train_generator,
        epochs=args.epochs,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )

    # 4. Phase 2: Fine-Tuning Top 35 Layers
    if args.fine_tune_epochs > 0:
        print(f"\n[3/3] Phase 2: Fine-Tuning Top 35 Layers of MobileNetV2 ({args.fine_tune_epochs} epochs)...")
        base_model.trainable = True
        for layer in base_model.layers[:-35]:
            layer.trainable = False

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )

        history_finetune = model.fit(
            train_generator,
            epochs=args.fine_tune_epochs,
            validation_data=val_generator,
            callbacks=callbacks,
            verbose=1
        )

    # 5. Save Model to Primary Locations
    primary_save_path = ARCHIVE_DIR / "tomato_disease_model.keras"
    backup_save_path = SAVED_MODELS_DIR / "tomato_disease_mobilenet.keras"
    class_names_path = SAVED_MODELS_DIR / "tomato_disease_class_names.json"

    model.save(str(primary_save_path))
    model.save(str(backup_save_path))
    print(f"\n Successfully saved high-accuracy model to: {primary_save_path}")
    print(f" Successfully saved backup model to: {backup_save_path}")

    class_list = [c for c, _ in sorted_classes]
    with open(class_names_path, "w") as f:
        json.dump({
            "model_name": "TomatoGuard_Disease_Classifier",
            "architecture": "MobileNetV2",
            "input_shape": [224, 224, 3],
            "num_classes": len(class_list),
            "classes": class_list,
            "class_indices": class_indices
        }, f, indent=4)
    print(f" Successfully saved class metadata to: {class_names_path}")

    # 6. Comprehensive Validation Evaluation
    print("\n" + "=" * 70)
    print("             FINAL VALIDATION ACCURACY EVALUATION             ")
    print("=" * 70)
    val_loss, val_acc = model.evaluate(val_generator, verbose=0)
    print(f"Validation Loss     : {val_loss:.4f}")
    print(f"Validation Accuracy : {val_acc * 100:.2f}%")
    print("=" * 70)
    print(" TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
