"""
Copy trained model files to Android app assets folder
Run this after training to update the bundled model in the APK
"""

import shutil
import os

def copy_model_files():
    """Copy model files from models/ to Android assets/"""
    
    # Source files
    model_file = 'models/weed_detector.tflite'
    labels_file = 'models/labels.txt'
    info_file = 'weed_info.json'
    
    # Destination folder
    assets_folder = 'WeedDetectorApp/app/src/main/assets'
    
    # Check if source files exist
    if not os.path.exists(model_file):
        print(f"Error: {model_file} not found. Train the model first!")
        return False
    
    if not os.path.exists(labels_file):
        print(f"Error: {labels_file} not found. Train the model first!")
        return False
    
    if not os.path.exists(info_file):
        print(f"Error: {info_file} not found!")
        return False
    
    # Create assets folder if it doesn't exist
    os.makedirs(assets_folder, exist_ok=True)
    
    # Copy files
    print("Copying model files to Android assets...")
    
    try:
        shutil.copy2(model_file, os.path.join(assets_folder, 'weed_detector.tflite'))
        print(f"  [OK] Copied {model_file}")
        
        shutil.copy2(labels_file, os.path.join(assets_folder, 'labels.txt'))
        print(f"  [OK] Copied {labels_file}")
        
        shutil.copy2(info_file, os.path.join(assets_folder, 'weed_info.json'))
        print(f"  [OK] Copied {info_file}")
        
        print("\n[SUCCESS] All files copied successfully!")
        print("\nNext steps:")
        print("1. Open Android Studio")
        print("2. Build > Rebuild Project")
        print("3. Run app on device")
        print("\nThe new model with updated weed information is now bundled in the app!")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Failed to copy files: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("COPY MODEL FILES TO ANDROID APP")
    print("=" * 60)
    print()
    
    success = copy_model_files()
    
    if not success:
        print("\nPlease fix the errors and try again.")
        exit(1)
