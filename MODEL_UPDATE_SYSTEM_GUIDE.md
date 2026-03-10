# Model Update System Guide

## Overview
The Green Scan app now supports automatic model updates! You can train new weed types and push updates to all users without rebuilding the APK.

## How It Works

### 1. Training New Weeds
1. Add new weed images to `dataset/weeds/[weed_name]/` folder
2. Run training from admin panel or command line
3. New model files are generated in `models/` folder

### 2. Publishing Updates
1. Login to admin panel (http://your-ip:5000/admin)
2. Go to "Model Training" section
3. After training completes, click "📤 Publish Model Update"
4. Model version is incremented (e.g., v1 → v2)

### 3. App Updates Automatically
1. App checks for updates when opened (once per day)
2. If new version available, user is notified
3. User can download update with one tap
4. New model is downloaded and used immediately
5. No APK reinstall needed!

## System Architecture

### Server Side (unified_admin_server.py)
- `/model/version` - Returns current model version number
- `/model/download/model` - Downloads weed_detector.tflite
- `/model/download/labels` - Downloads labels.txt
- `/model/download/info` - Downloads weed_info.json
- `/admin/model/publish` - Increments version (admin only)

### Android Side
- `ModelUpdateManager.java` - Handles update checking and downloading
- `WeedDetector.java` - Loads models from internal storage if available
- Models stored in app's internal storage (`/data/data/com.example.weeddetector/files/`)

## Workflow

### Adding New Weed Type

1. **Prepare Dataset**
   ```cmd
   python add_new_weed_class.py
   ```
   - Enter weed name (e.g., "cogon_grass")
   - Add 200-1000 images to `dataset/weeds/cogon_grass/`

2. **Train Model**
   - Option A: Admin Panel
     - Go to http://your-ip:5000/admin/training
     - Click "Start Training"
     - Wait for completion
   
   - Option B: Command Line
     ```cmd
     python train_model.py
     ```

3. **Publish Update**
   - In admin panel, click "📤 Publish Model Update"
   - Confirms model version increment
   - Users will be notified on next app open

4. **Users Get Update**
   - User opens app
   - Sees notification: "New model available (v2)"
   - Taps "Update Now"
   - Model downloads in background
   - App automatically uses new model
   - Can now detect the new weed type!

## Model Version Tracking

### model_version.json (Server)
```json
{
  "version": 2,
  "updated_at": "2026-03-02T12:00:00",
  "weed_types": 6
}
```

### SharedPreferences (Android)
- Stores current installed model version
- Compares with server version
- Triggers update if server version is higher

## File Locations

### Server Files
```
models/
  ├── weed_detector.tflite  (5MB model file)
  ├── labels.txt             (list of weed names)
  └── best_model.h5          (original Keras model)
weed_info.json               (weed descriptions)
model_version.json           (version tracking)
```

### Android App Files
```
assets/                      (bundled with APK)
  ├── weed_detector.tflite   (default model v1)
  ├── labels.txt
  └── weed_info.json

/data/data/.../files/        (downloaded updates)
  ├── weed_detector.tflite   (updated model v2+)
  ├── labels.txt
  └── weed_info.json
```

## Update Priority
1. Check `/data/data/.../files/` for downloaded model
2. If exists, use downloaded model (latest version)
3. If not exists, use bundled assets (default version)

## Benefits

✓ No APK rebuild needed
✓ No Google Play Store update required
✓ Instant deployment to all users
✓ Users always have latest weed detection
✓ Easy to add new weed types
✓ Centralized model management
✓ Version tracking and rollback capability

## Testing the System

### 1. Test Server Endpoints
```cmd
# Check version
curl http://localhost:5000/model/version

# Download model
curl http://localhost:5000/model/download/model -o test_model.tflite

# Download labels
curl http://localhost:5000/model/download/labels -o test_labels.txt
```

### 2. Test Android Update
1. Install app with v1 model
2. Train new model on server
3. Publish update (increments to v2)
4. Open app
5. Should see update notification
6. Download update
7. Restart app
8. New model should be active

## Manual Update Check

Users can manually check for updates:
1. Open app
2. Go to Settings (if implemented)
3. Tap "Check for Updates"
4. Download if available

## Automatic Update Check

- Checks once per day automatically
- Runs on app startup
- Non-intrusive notification
- User can choose to update or skip

## Future Enhancements

### Planned Features
- [ ] Update progress bar
- [ ] Model size display before download
- [ ] Update history/changelog
- [ ] Rollback to previous version
- [ ] Delta updates (only changed files)
- [ ] Background download
- [ ] WiFi-only download option
- [ ] Update scheduling

### Advanced Features
- [ ] A/B testing different models
- [ ] Regional model variants
- [ ] Compressed model downloads
- [ ] Incremental model updates
- [ ] Model performance analytics

## Troubleshooting

### Update Not Showing
- Check server is running
- Verify model version incremented
- Check app has internet permission
- Ensure phone and server on same network

### Download Fails
- Check file permissions
- Verify sufficient storage space
- Check network connectivity
- Try manual download from browser

### Model Not Loading
- Check file integrity
- Verify all 3 files downloaded
- Clear app data and retry
- Check logcat for errors

## Security Considerations

- Model files served over HTTP (use HTTPS in production)
- No authentication on download endpoints (public access)
- Version file can be cached
- Consider adding checksum verification
- Implement signature verification for production

## Production Deployment

For production use:
1. Use HTTPS for all endpoints
2. Add authentication for admin endpoints
3. Implement file checksums
4. Add download retry logic
5. Monitor download analytics
6. Set up CDN for model files
7. Implement rate limiting
8. Add error reporting

## Summary

The model update system allows you to:
1. Train new weed types anytime
2. Publish updates with one click
3. Users get updates automatically
4. No APK rebuild or store update needed
5. Always have the latest AI model

This makes your app future-proof and easily maintainable!
