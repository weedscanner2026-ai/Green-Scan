# Quick Fix for Gradle Issues

## The Problem
Your Gradle cache is corrupted and JAVA_HOME is misconfigured.

## Solution: Use Android Studio's Embedded Tools

### Step 1: Fix JAVA_HOME (Do this first!)
1. Press `Windows + R`
2. Type `sysdm.cpl` and press Enter
3. Click "Advanced" tab
4. Click "Environment Variables"
5. In "System variables", find `JAVA_HOME`
6. Edit it: Change from `C:\jdk-19.0.2\bin` to `C:\jdk-19.0.2`
7. Click OK on all dialogs
8. **Restart your computer** (or at least restart Android Studio)

### Step 2: Configure Android Studio
1. Open Android Studio
2. **Don't open the project yet!**
3. Go to File → Settings (or Configure → Settings from welcome screen)
4. Navigate to: Build, Execution, Deployment → Build Tools → Gradle
5. Set these options:
   - **Use Gradle from**: Select "Gradle wrapper"
   - **Gradle JDK**: Select "Embedded JDK" (or jbr-17 if available)
6. Click Apply and OK

### Step 3: Open Project Fresh
1. File → Open
2. Select `WeedDetectorApp` folder
3. Click OK
4. When prompted "Trust Gradle Project?", click "Trust Project"
5. Wait for Gradle sync (this will download fresh files)
6. **Be patient** - first sync takes 5-10 minutes

### Step 4: If Sync Still Fails
Try offline mode:
1. File → Settings → Build, Execution, Deployment → Gradle
2. Check "Offline work"
3. Click Apply
4. File → Sync Project with Gradle Files

If that doesn't work, uncheck "Offline work" and try again.

### Step 5: Alternative - Use Different Network
The "Tag mismatch" error often happens with:
- Unstable internet connection
- Corporate firewalls
- VPN interference
- Antivirus blocking downloads

Try:
- Disable VPN if you're using one
- Temporarily disable antivirus
- Use mobile hotspot instead of WiFi
- Try at a different location/network

### Step 6: Last Resort - Manual Gradle Setup
If nothing works, download Gradle manually:

1. Go to: https://gradle.org/releases/
2. Download Gradle 8.5 (binary-only)
3. Extract to: `C:\Gradle\gradle-8.5`
4. In Android Studio:
   - Settings → Build Tools → Gradle
   - Select "Use Gradle from: 'specified location'"
   - Browse to: `C:\Gradle\gradle-8.5`
   - Gradle JDK: Embedded JDK
5. Try syncing again

## Verify Model Files
Make sure these exist in `WeedDetectorApp/app/src/main/assets/`:
```
weed_detector.tflite  (4.96 MB)
labels.txt            (small text file)
weed_info.json        (JSON file)
```

## After Successful Build
1. Connect Android phone via USB
2. Enable Developer Options and USB Debugging on phone
3. Click green "Run" button in Android Studio
4. Select your device
5. App will install and launch

## Still Having Issues?
The project files are all correct. The issue is with your local Gradle/Java setup. Consider:
1. Reinstalling Android Studio
2. Using a different computer
3. Building on a different network
