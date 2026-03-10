# Web-Based Dataset Management Guide

## Overview
You can now add new weed classes directly from the admin web panel - no more command line needed!

## Accessing Dataset Management

1. **Login to Admin Panel**
   ```
   http://your-ip:5000/admin
   Username: admin
   Password: admin123
   ```

2. **Navigate to Dataset Management**
   - Click "📁 Dataset Management" in the side menu

## Adding New Weed Class

### Step 1: Fill Out the Form

The form has the following fields:

#### Required Fields (marked with *)
- **Weed Name**: Use lowercase with underscores (e.g., `cogon_grass`)
- **Scientific Name**: Latin name (e.g., `Imperata cylindrica`)
- **Description**: Brief description of the weed
- **Control Methods**: How to control/remove this weed

#### Optional Fields
- **Family**: Plant family (e.g., `Poaceae`)
- **Identification Features**: Key features for identification
- **Habitat**: Where it typically grows
- **Growth Season**: When it grows (e.g., `Year-round`)
- **Toxicity**: Select from dropdown (Non-toxic, Mildly toxic, etc.)

### Step 2: Submit Form

1. Click "Create Weed Class" button
2. System creates folder: `dataset/weeds/[weed_name]/`
3. System updates `weed_info.json` with your information
4. Success message shows folder location

### Step 3: Add Images

1. Click "📁 Open Folder" button next to the new weed class
2. File Explorer opens automatically
3. Add 200-1000 images to the folder
4. Supported formats: JPG, JPEG, PNG

### Step 4: Train Model

1. Go to "🤖 Model Training" section
2. Click "Start Training"
3. Wait for training to complete

### Step 5: Publish Update

1. Click "📤 Publish Model Update"
2. All app users will be notified
3. Users can download the new model

## Example: Adding Cogon Grass

### Fill the Form:
```
Weed Name: cogon_grass
Scientific Name: Imperata cylindrica
Family: Poaceae
Description: A perennial grass with sharp-edged leaves and white fluffy seed heads. Highly invasive and difficult to control.
Identification: Sharp leaf edges, white cylindrical flower spikes, extensive rhizome system
Habitat: Disturbed areas, roadsides, agricultural fields
Growth Season: Year-round in tropical climates
Control Methods: Deep plowing to remove rhizomes, herbicide application (glyphosate), repeated mowing to exhaust root reserves
Toxicity: Non-toxic
```

### After Submission:
1. Folder created: `dataset/weeds/cogon_grass/`
2. Click "Open Folder"
3. Add 500 cogon grass images
4. Train model
5. Publish update
6. Done!

## Current Dataset View

The page shows:
- **Total Classes**: Number of weed types
- **Total Images**: Sum of all images
- **Table**: List of all weed classes with:
  - Weed name
  - Image count
  - Status badge (Good/Fair/Low)
  - Open Folder button

### Status Badges:
- 🟢 **Good**: 200+ images
- 🟡 **Fair**: 100-199 images
- 🔴 **Low**: Less than 100 images

## Benefits of Web Interface

✓ No command line needed
✓ User-friendly form
✓ Validation built-in
✓ One-click folder opening
✓ Visual dataset overview
✓ Real-time statistics
✓ Error handling
✓ Success confirmation

## Tips

1. **Naming Convention**: Always use lowercase with underscores
   - ✓ Good: `cogon_grass`, `purple_nutsedge`
   - ✗ Bad: `Cogon Grass`, `cogon-grass`, `CogonGrass`

2. **Image Quality**: 
   - Clear, well-lit photos
   - Various angles and growth stages
   - Different backgrounds
   - Mix of close-up and distant shots

3. **Image Quantity**:
   - Minimum: 200 images
   - Recommended: 500+ images
   - More images = better accuracy

4. **Scientific Names**: 
   - Use proper Latin names
   - Include genus and species
   - Check spelling carefully

5. **Descriptions**:
   - Be specific and detailed
   - Include distinguishing features
   - Mention growth habits
   - Note any special characteristics

## Workflow Comparison

### Old Way (Command Line):
```cmd
1. python add_new_weed_class.py
2. Enter weed name
3. Enter scientific name
4. Enter description
5. Enter family
6. Enter identification
7. Enter habitat
8. Enter control methods
9. Enter toxicity
10. Enter growth season
11. Manually navigate to folder
12. Add images
```

### New Way (Web Interface):
```
1. Open admin panel
2. Click Dataset Management
3. Fill form (all fields visible at once)
4. Click Create
5. Click Open Folder
6. Add images
```

Much faster and easier!

## Troubleshooting

### "Weed class already exists"
- Choose a different name
- Or delete the existing folder first

### "Folder not opening"
- Check Windows File Explorer is working
- Try manually navigating to `dataset/weeds/[weed_name]/`

### "Form validation error"
- Check weed name uses only lowercase and underscores
- Ensure required fields are filled
- Check for special characters

### "Can't access page"
- Ensure you're logged in as admin
- Check server is running
- Verify network connection

## Security Note

Only admin users can access Dataset Management. Regular users cannot add or modify weed classes.

## Next Steps After Adding Weed

1. ✓ Create weed class (web form)
2. ✓ Add images (200-1000)
3. ✓ Train model (Model Training page)
4. ✓ Test model (optional)
5. ✓ Publish update (one click)
6. ✓ Users download automatically

## Summary

The web-based dataset management makes it incredibly easy to:
- Add new weed types
- View current dataset
- Manage weed information
- Open folders quickly
- Track image counts
- Monitor dataset health

No more command line - everything is visual and user-friendly!
