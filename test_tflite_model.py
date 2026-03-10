"""
Test TFLite model before Android deployment
"""

import tensorflow as tf
import numpy as np
from PIL import Image
import os
import time

def test_tflite_model(model_path='models/weed_detector.tflite', 
                     labels_path='models/labels.txt',
                     test_image_path=None):
    """Test TFLite model inference"""
    
    print("\n" + "="*60)
    print("TFLITE MODEL TESTING")
    print("="*60)
    
    # Check files exist
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        print("Run: python train_model.py")
        return False
    
    if not os.path.exists(labels_path):
        print(f"\n❌ Labels not found: {labels_path}")
        return False
    
    # Load labels
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    
    print(f"\n✓ Model: {model_path}")
    print(f"✓ Labels: {len(labels)} classes")
    print(f"✓ Model size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
    
    # Load TFLite model
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    # Get input/output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    input_shape = input_details[0]['shape']
    print(f"\nModel input shape: {input_shape}")
    print(f"Model output shape: {output_details[0]['shape']}")
    
    # Find a test image if not provided
    if test_image_path is None:
        print("\nSearching for test image...")
        for weed in labels:
            weed_dir = os.path.join('dataset/weeds', weed)
            if os.path.exists(weed_dir):
                images = [f for f in os.listdir(weed_dir) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if images:
                    test_image_path = os.path.join(weed_dir, images[0])
                    print(f"✓ Using: {test_image_path}")
                    break
    
    if test_image_path is None or not os.path.exists(test_image_path):
        print("\n⚠ No test image found. Model structure validated but inference not tested.")
        return True
    
    # Test inference
    print("\n" + "-"*60)
    print("Testing inference...")
    print("-"*60)
    
    # Load and preprocess image
    img = Image.open(test_image_path).convert('RGB')
    img = img.resize((input_shape[1], input_shape[2]))
    img_array = np.array(img, dtype=np.float32)
    
    # Normalize (same as training)
    img_array = img_array / 127.5 - 1.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Run inference multiple times to test speed
    times = []
    for i in range(10):
        start = time.time()
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])
        times.append(time.time() - start)
    
    # Get prediction
    predictions = output[0]
    predicted_idx = np.argmax(predictions)
    confidence = predictions[predicted_idx] * 100
    
    print(f"\nTest image: {test_image_path}")
    print(f"Predicted: {labels[predicted_idx]}")
    print(f"Confidence: {confidence:.2f}%")
    
    # Show top 3 predictions
    top_3_idx = np.argsort(predictions)[-3:][::-1]
    print("\nTop 3 predictions:")
    for idx in top_3_idx:
        print(f"  {labels[idx]:20s}: {predictions[idx]*100:5.2f}%")
    
    # Performance stats
    avg_time = np.mean(times) * 1000
    print(f"\nInference time: {avg_time:.1f} ms (avg of 10 runs)")
    print(f"FPS: {1000/avg_time:.1f}")
    
    # Validation checks
    print("\n" + "="*60)
    print("VALIDATION CHECKS")
    print("="*60)
    
    checks_passed = True
    
    # Check 1: Model size
    model_size_mb = os.path.getsize(model_path) / (1024*1024)
    if model_size_mb > 50:
        print(f"⚠ Model size is large: {model_size_mb:.2f} MB (may be slow on mobile)")
    else:
        print(f"✓ Model size OK: {model_size_mb:.2f} MB")
    
    # Check 2: Inference speed
    if avg_time > 1000:
        print(f"⚠ Inference slow: {avg_time:.1f} ms (may lag on mobile)")
    else:
        print(f"✓ Inference speed OK: {avg_time:.1f} ms")
    
    # Check 3: Output format
    if len(predictions) == len(labels):
        print(f"✓ Output classes match labels: {len(labels)}")
    else:
        print(f"❌ Output mismatch: {len(predictions)} outputs vs {len(labels)} labels")
        checks_passed = False
    
    # Check 4: Confidence scores
    if np.sum(predictions) > 0.99 and np.sum(predictions) < 1.01:
        print(f"✓ Output is valid probability distribution")
    else:
        print(f"⚠ Output sum: {np.sum(predictions):.4f} (should be ~1.0)")
    
    print("\n" + "="*60)
    if checks_passed:
        print("✓ MODEL READY FOR ANDROID DEPLOYMENT")
        print("\nNext steps:")
        print("1. Copy models/weed_detector.tflite → android/app/src/main/assets/")
        print("2. Copy models/labels.txt → android/app/src/main/assets/")
        print("3. Copy weed_info.json → android/app/src/main/assets/")
        print("4. Build and test Android app")
    else:
        print("❌ MODEL HAS ISSUES")
        print("Please retrain or check model configuration")
    
    return checks_passed

if __name__ == "__main__":
    import sys
    
    test_image = sys.argv[1] if len(sys.argv) > 1 else None
    success = test_tflite_model(test_image_path=test_image)
    exit(0 if success else 1)
