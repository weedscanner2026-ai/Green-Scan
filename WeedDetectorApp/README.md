# Philippine Green Scan Android App

AI-powered mobile app to identify Philippine weeds using your phone camera.

## Features

- 📷 Real-time weed detection using camera
- 🌿 Identifies 4 common Philippine weeds:
  - Crabgrass (Damong-alat)
  - Makahiya (Sensitive Plant)
  - Morsikos (Spanish Needle)
  - Teki (Nutsedge)
- 📊 Shows confidence percentage
- 📖 Detailed information for each weed:
  - Scientific name
  - Description
  - Identification tips
  - Habitat
  - Control methods
  - Toxicity information
  - Growth season

## How to Build

### Prerequisites
- Android Studio (latest version)
- Android SDK 24 or higher
- Java 8 or higher

### Steps

1. **Open in Android Studio**
   - Launch Android Studio
   - Click "Open an Existing Project"
   - Navigate to `WeedDetectorApp` folder
   - Click "OK"

2. **Sync Gradle**
   - Android Studio will automatically sync Gradle
   - Wait for the sync to complete
   - If prompted, accept any SDK updates

3. **Build the App**
   - Click "Build" → "Make Project" (or press Ctrl+F9)
   - Wait for the build to complete

4. **Run on Device/Emulator**
   - Connect your Android phone via USB (enable USB debugging)
   - OR start an Android emulator
   - Click the "Run" button (green play icon)
   - Select your device
   - The app will install and launch

## Model Files

The following files are already included in `app/src/main/assets/`:
- `weed_detector.tflite` - Trained TensorFlow Lite model (4.96 MB)
- `labels.txt` - Weed class labels
- `weed_info.json` - Detailed weed information database

## App Structure

```
WeedDetectorApp/
├── app/
│   ├── src/main/
│   │   ├── java/com/example/weeddetector/
│   │   │   ├── MainActivity.java       # Main UI and camera handling
│   │   │   └── WeedDetector.java       # TensorFlow Lite inference
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   └── activity_main.xml   # UI layout
│   │   │   └── values/
│   │   │       └── strings.xml
│   │   ├── assets/
│   │   │   ├── weed_detector.tflite
│   │   │   ├── labels.txt
│   │   │   └── weed_info.json
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
└── settings.gradle
```

## Usage

1. Launch the app
2. Grant camera permission when prompted
3. Tap "📷 Scan Weed" button
4. Take a photo of the weed
5. View the detection results with detailed information

## Model Performance

- Accuracy: ~90%+ on validation set
- Inference time: ~14ms per image
- Model size: 4.96 MB
- Trained on 4,304 images

## Troubleshooting

### Build Errors
- Make sure you have Android SDK 24+ installed
- Sync Gradle files: File → Sync Project with Gradle Files
- Clean and rebuild: Build → Clean Project, then Build → Rebuild Project

### Camera Not Working
- Check camera permissions in app settings
- Ensure your device has a working camera
- Try restarting the app

### Model Not Loading
- Verify all files exist in `app/src/main/assets/`
- Check file sizes match the originals
- Rebuild the project

## Future Improvements

- Add more weed types
- Implement gallery image selection
- Add offline mode
- Include weed distribution maps
- Multi-language support (Tagalog, Cebuano, etc.)

## License

This project is for educational purposes.
