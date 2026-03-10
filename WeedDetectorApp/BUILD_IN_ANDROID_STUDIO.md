# Build Instructions for Android Studio

## Error Fixed
✓ Fixed JSONException error in LoginActivity.java

## Steps to Build

### 1. Open Project in Android Studio
1. Launch Android Studio
2. Click "Open"
3. Navigate to: `WeedDetectorApp` folder
4. Click "OK"

### 2. Wait for Gradle Sync
- Android Studio will automatically sync Gradle
- Wait for "Gradle sync finished" message
- This may take a few minutes on first open

### 3. Update Server IP Address
1. Open: `app/src/main/java/com/example/weeddetector/ApiConfig.java`
2. Find this line:
   ```java
   private static final String SERVER_IP = "192.168.1.100"; // CHANGE THIS!
   ```
3. Replace with YOUR computer's IP address
4. Save the file (Ctrl+S)

### 4. Build the Project
1. Click: **Build** > **Rebuild Project**
2. Wait for build to complete
3. Check "Build" tab at bottom for any errors

### 5. Run on Device
1. Connect your Android phone via USB
2. Enable USB Debugging on phone:
   - Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > Developer Options
   - Enable "USB Debugging"
3. Click the green "Run" button (▶) in Android Studio
4. Select your device
5. Click "OK"

## Common Issues

### Issue: "SDK not found"
**Solution:**
1. File > Project Structure
2. SDK Location tab
3. Set Android SDK location
4. Click "Apply"

### Issue: "Build failed"
**Solution:**
1. Check "Build" tab for specific errors
2. Try: Build > Clean Project
3. Then: Build > Rebuild Project

### Issue: "Gradle sync failed"
**Solution:**
1. File > Invalidate Caches / Restart
2. Click "Invalidate and Restart"
3. Wait for Android Studio to restart

### Issue: "Cannot resolve symbol"
**Solution:**
1. File > Sync Project with Gradle Files
2. Wait for sync to complete

## Verify Build Success

After successful build, you should see:
- ✓ "BUILD SUCCESSFUL" in Build tab
- ✓ APK created in: `app/build/outputs/apk/debug/`
- ✓ App installs on phone
- ✓ App opens to Login screen

## Testing the App

### 1. Start Registration Server
On your computer:
```bash
python registration_server.py
```

### 2. Test Registration
1. Open app on phone
2. Click "Don't have an account? Register"
3. Fill in registration form
4. Click "Register"
5. Should see: "Registration successful!"

### 3. Test Login
1. Enter username and password
2. Click "Login"
3. Should redirect to scanner screen

### 4. Test Scanning
1. Tap "Scan" button
2. Take photo of a weed
3. View detection results

## Files Modified

✓ `LoginActivity.java` - Fixed JSONException
✓ `RegisterActivity.java` - User registration
✓ `ApiConfig.java` - Server configuration
✓ `AndroidManifest.xml` - Added activities and permissions
✓ `activity_login.xml` - Login layout
✓ `activity_register.xml` - Registration layout

## Next Steps After Build

1. ✓ Build successful
2. ✓ App installed on phone
3. ✓ Server running on computer
4. ✓ Phone and computer on same WiFi
5. ✓ Test registration
6. ✓ Test login
7. ✓ Test weed scanning
8. ✓ Check admin dashboard

## Admin Dashboard

While testing, view registered users:
1. Open browser: http://localhost:5000/admin/login
2. Login: admin / admin123
3. See all registered users

## Success Checklist

- [ ] Android Studio opened project
- [ ] Gradle sync completed
- [ ] Updated ApiConfig.java with IP
- [ ] Build successful
- [ ] App installed on phone
- [ ] Registration server running
- [ ] App shows login screen
- [ ] Registration works
- [ ] Login works
- [ ] Scanner works
- [ ] Admin dashboard shows users

## Need Help?

1. Check Android Studio Logcat for errors
2. Verify phone and computer on same WiFi
3. Check firewall allows port 5000
4. Review QUICK_START_REGISTRATION.md

---

**Ready to build!** Open Android Studio and follow the steps above.
