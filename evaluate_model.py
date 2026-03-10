"""
Script to evaluate trained model and visualize results
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import os

def load_model_and_data(model_path='models/best_model.h5', data_dir='dataset/weeds'):
    """Load trained model and validation dataset"""
    model = keras.models.load_model(model_path)
    
    val_ds = keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(224, 224),
        batch_size=32
    )
    
    return model, val_ds

def evaluate_accuracy(model, val_ds):
    """Evaluate model accuracy"""
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    results = model.evaluate(val_ds)
    print(f"\nValidation Loss: {results[0]:.4f}")
    print(f"Validation Accuracy: {results[1]*100:.2f}%")
    
    return results

def plot_confusion_matrix(model, val_ds, class_names):
    """Generate and plot confusion matrix"""
    y_true = []
    y_pred = []
    
    for images, labels in val_ds:
        predictions = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(predictions, axis=1))
    
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('models/confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("\n✓ Confusion matrix saved to models/confusion_matrix.png")

def generate_classification_report(model, val_ds, class_names):
    """Generate detailed classification report"""
    y_true = []
    y_pred = []
    
    for images, labels in val_ds:
        predictions = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(predictions, axis=1))
    
    print("\n" + "="*60)
    print("CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    # Save to file
    report = classification_report(y_true, y_pred, target_names=class_names)
    with open('models/classification_report.txt', 'w') as f:
        f.write(report)
    print("\n✓ Report saved to models/classification_report.txt")

def test_single_image(model, image_path, class_names):
    """Test model on a single image"""
    img = keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 127.5 - 1  # Normalize
    
    predictions = model.predict(img_array, verbose=0)
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0]) * 100
    
    print(f"\nPrediction: {predicted_class}")
    print(f"Confidence: {confidence:.2f}%")
    
    # Show top 3 predictions
    top_3_idx = np.argsort(predictions[0])[-3:][::-1]
    print("\nTop 3 predictions:")
    for idx in top_3_idx:
        print(f"  {class_names[idx]}: {predictions[0][idx]*100:.2f}%")

if __name__ == "__main__":
    # Load model and data
    model, val_ds = load_model_and_data()
    class_names = val_ds.class_names
    
    # Evaluate
    evaluate_accuracy(model, val_ds)
    
    # Generate reports
    plot_confusion_matrix(model, val_ds, class_names)
    generate_classification_report(model, val_ds, class_names)
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
    print("\nCheck models/ folder for:")
    print("  - confusion_matrix.png")
    print("  - classification_report.txt")
