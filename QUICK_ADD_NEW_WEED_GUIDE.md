# Quick Guide: Adding New Weed Types

## Simple 4-Step Process

### Step 1: Create Folder & Add Images
```cmd
python add_new_weed_class.py
```
- Enter weed name (e.g., "cogon_grass")
- Add 200-1000 images to `dataset/weeds/cogon_grass/`

### Step 2: Train Model
Open admin panel: http://your-ip:5000/admin/training
- Click "Start Training"
- Wait for completion (shows progress)

### Step 3: Publish Update
In admin panel:
- Click "📤 Publish Model Update"
- Confirms version increment

### Step 4: Users Get Update
Users open app:
- See "Update Available" notification
- Tap "Update Now"
- New weed type ready to detect!

## That's It!

No APK rebuild needed. No app store update. Users get new weed detection automatically!

## Example: Adding "Cogon Grass"

1. **Create dataset**
   ```cmd
   python add_new_weed_class.py
   # Enter: cogon_grass
   # Enter scientific name, description, etc.
   ```

2. **Add images**
   - Download 500 cogon grass images
   - Put in `dataset/weeds/cogon_grass/`

3. **Train**
   - Admin panel → Model Training
   - Start Training
   - Wait ~10-30 minutes

4. **Publish**
   - Click "Publish Model Update"
   - Done!

5. **Users update**
   - Open app
   - "Update Available (v2)"
   - Download
   - Can now detect cogon grass!

## Current Weeds in Model

1. Crabgrass (927 images)
2. Makahiya (1,290 images)
3. Morsikos (1,044 images)
4. Teki (1,043 images)
5. Not Weed (33 images)

## Adding More Weeds

Want to add 5 more weeds?

1. Create 5 folders in `dataset/weeds/`
2. Add images to each (200+ per weed)
3. Train once
4. Publish once
5. All users get all 5 new weeds!

## Tips

- More images = better accuracy (aim for 500+)
- Vary lighting, angles, backgrounds
- Include different growth stages
- Mix close-up and distant shots
- Train on good computer (faster)
- Publish after testing model works

## Server Must Be Running

For users to get updates:
```cmd
python unified_admin_server.py
```

Keep server running on your network. Users need internet access to download updates.

## Future-Proof

This system means your app can grow forever:
- Add Philippine weeds as you discover them
- Update descriptions and info
- Improve model accuracy
- No limit on weed types
- Always up-to-date for all users
