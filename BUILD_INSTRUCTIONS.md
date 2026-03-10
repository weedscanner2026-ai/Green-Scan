# How to Build the Green Scan App

## Fix JAVA_HOME First (Important!)

Your JAVA_HOME is currently set incorrectly. Fix it:

1. Press Windows + R
2. Type `sysdm.cpl` and press Enter
3. Go to "Advanced" tab → "Environment Variables"
4. Find `JAVA_HOME` in System Variables
5. Change from: `C:\jdk-19.0.2\bin`
6. Change to: `C:\jdk-19.0.2`
7. Click OK on all windows
8. Restart Android Studio

## Build in Android Studio

1. Open Android Studio
2. File → Open → Select `WeedDetectorApp` folder
3. Wait for indexing to complete
4. File → Settings → Build, Execution, Deployment → Build Tools → Gradle
5. Under "Gradle JDK", select "jdk-19" or "Embedded JDK"
6. Click Apply and OK
7. File → Sync Project with Gradle Files
8. Build → Make Project

## If Gradle Still Fails

Use Android Studio's built-in Gradle:
1. File → Settings → Build, Execution, Deployment → Gradle
2. Select "Use Gradle from: 'wrapper task in Gradle build script'"
3. Gradle JDK: Select your JDK 19 or use Embedded JDK
4. Click Apply

## Alternative: Import as New Project

1. File → New → Import Project
2. Select `WeedDetectorApp` folder
3. Choose "Import project from external model" → Gradle
4. Click Finish
5. Let Android Studio configure everything automatically

## Model Files Location

Make sure these files exist in `WeedDetectorApp/app/src/main/assets/`:
- weed_detector.tflite (4.96 MB)
- labels.txt
- weed_info.json

## Run the App

1. Connect your Android phone via USB
2. Enable USB Debugging on your phone
3. Click the green "Run" button in Android Studio
4. Select your device
5. App will install and launch

## Troubleshooting

### "JAVA_HOME is invalid"
- Fix JAVA_HOME as described above
- Restart Android Studio after changing

### "Could not download Gradle"
- Check your internet connection
- Try using Android Studio's embedded Gradle
- Or manually download Gradle and point to it in settings

### "SDK not found"
- Open SDK Manager (Tools → SDK Manager)
- Install Android SDK Platform 34
- Install Android SDK Build-Tools

### Build succeeds but app crashes
- Check that all 3 model files are in the assets folder
- Check file sizes match the originals
- Check Logcat for error messages
