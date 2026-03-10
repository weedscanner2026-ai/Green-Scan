# Model Update Troubleshooting Guide

## Problem: New Weed Detected But No Description

### Symptom
- App can detect new weed class (e.g., cogon_grass)
- Shows weed name correctly
- But description, scientific name, and control methods show "N/A" or "No information available"

### Root Cause
The app has two sources for weed information:

1. **Bundled in APK** (assets folder)
   - `weed_detector.tflite` - The AI model
   - `labels.txt` - List of weed names
   - `weed_info.json` - Weed descriptions

2. **Downloaded Updates** (internal storage)
   - Updated model files downloaded from server
   - Stored in `/data/data/com.example.weeddetector/files/`

**The Issue:** When you add a new weed and train:
- Server's `weed_info.json` gets updated ✓
- Model gets retrained with new class ✓
- BUT the Android app's bundled `weed_info.json` is outdated ✗

## Solution Options

### Option 1: Automatic Copy (Recommended)

The training script now automatically copies files to Android assets!

**Steps:**
```cmd
# 1. Add new weed class
python add_new_weed_class.py

# 2. Add images to dataset/weeds/[weed_name]/

# 3. Train model (auto-copies to Android)
python train_model.py

# 4. Rebuild Android app
Open Android Studio > Build > Rebuild Project

# 5. Install updated APK on device
```

### Option 2: Manual Copy

If automatic copy fails, copy manually:

**Steps:**
```cmd
# 1. Copy model file
copy models\weed_detector.tflite WeedDetectorApp\app\src\main\assets\

# 2. Copy labels file
copy models\labels.txt WeedDetectorApp\app\src\main\assets\

# 3. Copy weed info
copy weed_info.json WeedDetectorApp\app\src\main\assets\

# 4. Rebuild in Android Studio
```

### Option 3: Use Model Update System

For existing users without reinstalling:

**Steps:**
```cmd
# 1. Train model
python train_model.py

# 2. Publish update in admin panel
http://localhost:5000/admin/training
Click "📤 Publish Model Update"

# 3. Users download update
Users open app > See "Update Available" > Tap "Update Now"
```

**Note:** This downloads all 3 files to internal storage, overriding bundled files.

## Verification Steps

### Check Server Files
```cmd
# 1. Check weed_info.json has new weed
type weed_info.json | findstr "cogon_grass"

# 2. Check labels.txt has new weed
type models\labels.txt | findstr "cogon_grass"

# 3. Check model file exists
dir models\weed_detector.tflite
```

### Check Android Assets
```cmd
# 1. Check if files exist
dir WeedDetectorApp\app\src\main\assets\

# 2. Check weed_info.json content
type WeedDetectorApp\app\src\main\assets\weed_info.json | findstr "cogon_grass"
```

### Check App Behavior
1. Install/run app
2. Scan cogon grass image
3. Should show:
   - ✓ Weed name: "COGON_GRASS"
   - ✓ Scientific name: "Imperata cylindrica"
   - ✓ Description: Full description
   - ✓ Control methods: Detailed methods

## Common Issues

### Issue 1: Model Detects But Shows "Unknown"
**Cause:** `weed_info.json` doesn't have the weed entry
**Solution:** 
- Check `weed_info.json` has the weed
- Copy updated file to Android assets
- Rebuild app

### Issue 2: Shows "N/A" for All Fields
**Cause:** Weed name in `labels.txt` doesn't match key in `weed_info.json`
**Solution:**
- Check exact spelling in both files
- Ensure lowercase with underscores
- Example: `cogon_grass` (not `Cogon Grass` or `cogon-grass`)

### Issue 3: Old Information Still Showing
**Cause:** App using cached bundled files instead of updated ones
**Solution:**
- Clear app data: Settings > Apps > Green Scan > Clear Data
- Reinstall app
- Or download model update from server

### Issue 4: Update Downloaded But Still Shows Old Info
**Cause:** Downloaded files corrupted or incomplete
**Solution:**
- Check server is running
- Re-download update
- Check file sizes match server files

## File Synchronization Checklist

After adding new weed and training:

- [ ] `weed_info.json` (root) has new weed entry
- [ ] `models/labels.txt` has new weed name
- [ ] `models/weed_detector.tflite` is newly trained
- [ ] `WeedDetectorApp/app/src/main/assets/weed_info.json` updated
- [ ] `WeedDetectorApp/app/src/main/assets/labels.txt` updated
- [ ] `WeedDetectorApp/app/src/main/assets/weed_detector.tflite` updated
- [ ] Android app rebuilt
- [ ] APK installed on device
- [ ] Model update published on server (for existing users)

## Automated Copy Script

Use the provided script for easy copying:

```cmd
python copy_model_to_android.py
```

This script:
1. Checks if model files exist
2. Copies all 3 files to Android assets
3. Shows success/error messages
4. Provides next steps

## Best Practice Workflow

### For New APK Builds:
```
1. Add weed class
2. Train model (auto-copies to assets)
3. Rebuild Android app
4. Install new APK
5. Test detection
```

### For Existing Users:
```
1. Add weed class
2. Train model
3. Publish update in admin panel
4. Users download update in app
5. No reinstall needed
```

## Technical Details

### File Priority
The app loads files in this order:
1. Check internal storage (`/data/data/.../files/`)
2. If not found, use bundled assets
3. If neither, show "No information available"

### Update Process
When user downloads update:
1. Downloads `weed_detector.tflite` from server
2. Downloads `labels.txt` from server
3. Downloads `weed_info.json` from server
4. Saves all to internal storage
5. App restarts and loads from internal storage

### Why Both Locations?
- **Bundled (assets):** Default model, works offline, no download needed
- **Downloaded (internal):** Updated model, latest weeds, requires internet once

## Prevention

To avoid this issue in future:

1. **Always run training script** - It auto-copies files
2. **Or use copy script** - `python copy_model_to_android.py`
3. **Rebuild app after training** - Ensures latest files bundled
4. **Publish updates** - For existing users without reinstall
5. **Test before deploying** - Verify descriptions show correctly

## Quick Fix Commands

```cmd
# Quick fix for missing descriptions
python copy_model_to_android.py
cd WeedDetectorApp
gradlew assembleDebug
adb install -r app\build\outputs\apk\debug\app-debug.apk
```

## Summary

The issue occurs because:
- Training updates server files ✓
- But Android assets need manual/automatic copy ✗
- Solution: Copy files to assets and rebuild app ✓

Now the training script does this automatically!
