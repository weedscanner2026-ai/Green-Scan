import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import numpy as np
import os

# Model configuration
IMG_SIZE = 224
BATCH_SIZE = 16  # Smaller batch for better accuracy
EPOCHS = 100  # More epochs with early stopping

def create_model(num_classes):
    """Create an enhanced MobileNetV2-based model for high accuracy weed classification"""
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Fine-tune the last 30 layers
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False
    
    model = keras.Sequential([
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        # Data augmentation layers
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomContrast(0.2),
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def prepare_dataset(data_dir):
    """Load and prepare the dataset with preprocessing"""
    train_ds = keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE
    )
    
    val_ds = keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE
    )
    
    # Save class names before transformations
    class_names = train_ds.class_names
    
    # Normalize pixel values
    normalization_layer = layers.Rescaling(1./127.5, offset=-1)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
    
    # Performance optimization
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
    return train_ds, val_ds, class_names

def train_and_save_model(data_dir, output_dir='models'):
    """Train the model with high accuracy settings and save in TFLite format"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data
    print("Loading dataset...")
    train_ds, val_ds, class_names = prepare_dataset(data_dir)
    
    # Get number of classes
    num_classes = len(class_names)
    print(f"Found {num_classes} weed classes: {class_names}")
    
    # Create and compile model
    print("Building model...")
    model = create_model(num_classes)
    
    # Use learning rate schedule for better convergence
    initial_learning_rate = 0.001
    lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate,
        decay_steps=1000,
        decay_rate=0.9,
        staircase=True
    )
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr_schedule),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    # Callbacks for high accuracy
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        ModelCheckpoint(
            f'{output_dir}/best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train
    print("Training model...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    print("\nFinal Evaluation:")
    results = model.evaluate(val_ds)
    print(f"Validation Accuracy: {results[1]*100:.2f}%")
    print(f"Top-3 Accuracy: {results[2]*100:.2f}%")
    
    # Save as TFLite with optimization
    print("\nConverting to TensorFlow Lite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()
    
    tflite_path = f'{output_dir}/weed_detector.tflite'
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
    
    # Save labels
    labels_path = f'{output_dir}/labels.txt'
    with open(labels_path, 'w') as f:
        for name in class_names:
            f.write(f"{name}\n")
    
    print(f"\n[SUCCESS] Model saved to {tflite_path}")
    print(f"[SUCCESS] Labels saved to {labels_path}")
    print(f"[SUCCESS] Model size: {os.path.getsize(tflite_path) / (1024*1024):.2f} MB")
    
    # Auto-copy to Android assets if folder exists
    android_assets = 'WeedDetectorApp/app/src/main/assets'
    if os.path.exists('WeedDetectorApp'):
        try:
            print(f"\n[INFO] Copying files to Android assets...")
            os.makedirs(android_assets, exist_ok=True)
            
            import shutil
            shutil.copy2(tflite_path, os.path.join(android_assets, 'weed_detector.tflite'))
            shutil.copy2(labels_path, os.path.join(android_assets, 'labels.txt'))
            shutil.copy2('weed_info.json', os.path.join(android_assets, 'weed_info.json'))
            
            print(f"[SUCCESS] Files copied to Android assets!")
            print(f"[INFO] Rebuild the Android app to include new model")
        except Exception as e:
            print(f"[WARNING] Could not copy to Android assets: {e}")
    
    return model, history

if __name__ == "__main__":
    import sys
    
    # Check if dataset directory exists
    DATA_DIR = "dataset/weeds"
    if not os.path.exists(DATA_DIR):
        print(f"\n❌ Dataset directory not found: {DATA_DIR}")
        print("\nPlease follow these steps:")
        print("1. Read dataset_guide.md for collection guidelines")
        print("2. Run: python download_datasets.py")
        print("3. Collect/download images into dataset/weeds/ folder")
        print("4. Ensure minimum 100 images per weed type")
        print("5. Run this script again")
        sys.exit(1)
    
    # Check if dataset has enough images
    weed_folders = [f for f in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, f))]
    if len(weed_folders) == 0:
        print(f"\n❌ No weed folders found in {DATA_DIR}")
        print("Please add weed image folders first!")
        sys.exit(1)
    
    print(f"\nFound {len(weed_folders)} weed types:")
    for folder in weed_folders:
        img_count = len([f for f in os.listdir(os.path.join(DATA_DIR, folder)) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        status = "[OK]" if img_count >= 100 else "[!]"
        print(f"  {status} {folder}: {img_count} images")
    
    print("\nStarting training...")
    train_and_save_model(DATA_DIR)
