# -*- coding: utf-8 -*-
"""
Tomato Crop Disease Classification - CNN Training Script
Location: d:/tomato_crop/tomato-ai-system/ml/training/train.py
"""

import os
import sys
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Suppress excessive TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def build_model(input_shape=(128, 128, 3), num_classes=10):
    np.random.seed(1337)
    tf.random.set_seed(1337)
    
    model = Sequential([
        Input(shape=input_shape),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(16, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(8, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def main():
    parser = argparse.ArgumentParser(description="Train CNN on Tomato Leaf Disease Dataset")
    parser.add_argument('--epochs', type=int, default=5, help="Number of training epochs (default: 5)")
    parser.add_argument('--batch_size', type=int, default=64, help="Batch size (default: 64)")
    parser.add_argument('--steps_per_epoch', type=int, default=20, help="Steps per epoch (default: 20)")
    parser.add_argument('--val_steps', type=int, default=15, help="Validation steps per epoch (default: 15)")
    parser.add_argument('--train_dir', type=str, default=r'D:\archive\tomato\train', help="Path to train directory")
    parser.add_argument('--val_dir', type=str, default=r'D:\archive\tomato\val', help="Path to validation directory")
    args = parser.parse_args()

    print("=" * 65)
    print("      TOMATO LEAF DISEASE CLASSIFICATION - CNN TRAINING      ")
    print("=" * 65)
    print(f"TensorFlow Version : {tf.__version__}")
    print(f"Epochs             : {args.epochs}")
    print(f"Batch Size         : {args.batch_size}")
    print(f"Steps Per Epoch    : {args.steps_per_epoch}")
    print(f"Validation Steps   : {args.val_steps}")
    print("=" * 65)

    # Part 1 : Building the CNN
    print("\n[1/4] Building CNN Model Architecture...")
    classifier = build_model(input_shape=(128, 128, 3), num_classes=10)
    classifier.summary()

    # Part 2 : Preparing Data Generators
    print("\n[2/4] Loading and Augmenting Dataset...")
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    training_set = train_datagen.flow_from_directory(
        args.train_dir,
        target_size=(128, 128),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=True
    )

    label_map = training_set.class_indices
    print("\nDetected Class Mapping:")
    for class_name, idx in sorted(label_map.items(), key=lambda x: x[1]):
        print(f"  [{idx}] {class_name}")

    test_set = test_datagen.flow_from_directory(
        args.val_dir,
        target_size=(128, 128),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=False
    )

    # Part 3 : Model Training
    print(f"\n[3/4] Starting CNN Training for {args.epochs} epochs...")
    history = classifier.fit(
        training_set,
        steps_per_epoch=args.steps_per_epoch,
        epochs=args.epochs,
        validation_data=test_set,
        validation_steps=args.val_steps,
        verbose=1
    )

    # Part 4 : Save Model and Weights
    print("\n[4/4] Saving Trained Model Weights and Architecture...")
    weights_path = 'keras_potato_trained_model_weights.weights.h5'
    model_path = 'tomato_disease_model.keras'
    
    try:
        classifier.save_weights(weights_path)
        print(f" Successfully saved model weights as: {weights_path}")
    except Exception as e:
        print(f"Note on save_weights: {e}")
        
    try:
        classifier.save(model_path)
        print(f" Successfully saved complete model as: {model_path}")
    except Exception as e:
        print(f"Note on full model save: {e}")

    # Evaluation on Validation Set
    print("\n" + "=" * 65)
    print("                     EVALUATION SUMMARY                     ")
    print("=" * 65)
    val_loss, val_acc = classifier.evaluate(test_set, steps=args.val_steps, verbose=0)
    print(f"Final Validation Loss     : {val_loss:.4f}")
    print(f"Final Validation Accuracy : {val_acc * 100:.2f}%")
    print("=" * 65)
    print(" TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == '__main__':
    main()
