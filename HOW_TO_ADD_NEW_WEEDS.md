# How to Add New Weed Species to Your Dataset

## Overview
This guide shows you how to expand your weed detection model by adding new weed species.

---

## Quick Method (Using Script)

### Step 1: Run the Add Weed Script

```bash
python add_new_weed_class.py
```

### Step 2: Follow the Prompts

The script will ask you:
1. **Weed Name** (e.g., "Cogon Grass")
2. **Scientific Name** (e.g., "Imperata cylindrica")
3. **Common Names** (comma-separated)
4. **Plant Family**
5. **Description**
6. **How to Identify**
7. **Habitat**
8. **Control Methods**
9. **Toxicity**
10. **Growth Season**

### Step 3: Add Images

After running the script, add images to the created folder:
```
dataset/weeds/cogon_grass/
```

### Step 4: Retrain Model

```bash
python train_model.py
```

---

## Manual Method (Step by Step)

### Step 1: Create Folder for New Weed

Create a new folder in `dataset/weeds/` with the weed name:

```bash
# Example: Adding "Cogon Grass"
mkdir dataset\weeds\cogon_grass
```

**Naming Rules:**
- Use lowercase
- Replace spaces with underscores
- No special characters
- Examples:
  - "Cogon Grass" → `cogon_grass`
  - "Water Hyacinth" → `water_hyacinth`
  - "Madre de Cacao" → `madre_de_cacao`

### Step 2: Add Images to Folder

Put your weed images in the new folder:

```
dataset/weeds/cogon_grass/
├── cogon_001.jpg
├── cogon_002.jpg
├── cogon_003.jpg
└── ... (more images)
```

**Image Requirements:**
- **Minimum:** 200 images
- **Recommended:** 500-1000 images
- **Format:** JPG or PNG
- **Size:** Any size (will be resized automatically)

**Image Quality Tips:**
- ✓ Clear, well-lit photos
- ✓ Different angles (top, side, close-up)
- ✓ Various growth stages
- ✓ Different lighting conditions
- ✓ Include leaves, stems, flowers
- ✗ Avoid blurry images
- ✗ Avoid very dark images
- ✗ Avoid images with multiple weeds

### Step 3: Update weed_info.json

Open `weed_info.json` and add information about the new weed:

```json
{
  "weeds": {
    "cogon_grass": {
      "scientific_name": "Imperata cylindrica",
      "common_names": ["Cogon Grass", "Blady Grass", "Kunai Grass"],
      "family": "Poaceae",
      "description": "Perennial grass that forms dense stands. Sharp leaf edges. White fluffy seed heads. Very invasive.",
      "identification": "Sharp-edged leaves, white cylindrical flower spikes, grows 0.5-1.5m tall",
      "habitat": "Roadsides, abandoned fields, disturbed areas",
      "control_methods": "Herbicides (glyphosate), repeated mowing, root removal, burning with permits",
      "toxicity": "Non-toxic but sharp leaves can cut skin",
      "growth_season": "Year-round, flowers in dry season"
    },
    "existing_weed_1": { ... },
    "existing_weed_2": { ... }
  }
}
```

### Step 4: Verify Dataset Structure

Your dataset should look like this:

```
dataset/weeds/
├── crabgrass/          (927 images)
├── makahiya/           (1,290 images)
├── morsikos/           (1,044 images)
├── teki/               (1,043 images)
├── not_weed/           (33 images)
└── cogon_grass/        (NEW - your images)
```

### Step 5: Retrain the Model

Run the training script:

```bash
python train_model.py
```

The model will now train on 6 classes instead of 5!

### Step 6: Update Android App

After training completes:

```bash
# Copy new model files
copy models\weed_detector.tflite WeedDetectorApp\app\src\main\assets\
copy models\labels.txt WeedDetectorApp\app\src\main\assets\
copy weed_info.json WeedDetectorApp\app\src\main\assets\
```

### Step 7: Rebuild Android App

1. Open Android Studio
2. Build > Rebuild Project
3. Run on device
4. Test the new weed detection!

---

## Using Admin Panel to Train

Instead of terminal, you can use the web interface:

### Step 1: Add Images Manually

1. Create folder: `dataset/weeds/new_weed_name/`
2. Add images to the folder
3. Update `weed_info.json`

### Step 2: Start Admin Server

```bash
python unified_admin_server.py
```

### Step 3: Train via Web Interface

1. Go to: http://localhost:5000/admin/login
2. Login: admin / admin123
3. Click "Model Training" in sidebar
4. You'll see the new weed in dataset statistics
5. Set epochs (100 recommended)
6. Click "Start Training"
7. Watch progress in real-time!

---

## Example: Adding Multiple Weeds

Let's say you want to add 3 new weeds:

### 1. Cogon Grass

```bash
python add_new_weed_class.py
# Enter: Cogon Grass
# Fill in the information
# Add images to: dataset/weeds/cogon_grass/
```

### 2. Water Hyacinth

```bash
python add_new_weed_class.py
# Enter: Water Hyacinth
# Fill in the information
# Add images to: dataset/weeds/water_hyacinth/
```

### 3. Lantana

```bash
python add_new_weed_class.py
# Enter: Lantana
# Fill in the information
# Add images to: dataset/weeds/lantana/
```

### Then Retrain Once

```bash
python train_model.py
```

The model will now detect 8 classes:
1. crabgrass
2. makahiya
3. morsikos
4. teki
5. not_weed
6. cogon_grass (NEW)
7. water_hyacinth (NEW)
8. lantana (NEW)

---

## Where to Get Images

### Option 1: Take Your Own Photos
- Best option for accuracy
- Use your phone camera
- Take 200-500 photos per weed
- Vary angles and lighting

### Option 2: Download from Internet
- Google Images (search: "weed_name plant")
- iNaturalist.org
- PlantNet
- Wikimedia Commons
- Make sure images are copyright-free

### Option 3: Use Existing Datasets
- Kaggle datasets
- Agricultural research databases
- University plant databases

---

## Tips for Best Results

### Image Collection:
1. **Quantity:** More images = better accuracy
   - Minimum: 200 per class
   - Good: 500 per class
   - Excellent: 1000+ per class

2. **Quality:** Clear, focused images
   - Good lighting
   - Sharp focus
   - Proper framing

3. **Variety:** Different conditions
   - Young and mature plants
   - Different angles
   - Various backgrounds
   - Different times of day

### Training:
1. **Balanced Dataset:** Similar number of images per class
2. **More Epochs:** Use 100-150 epochs for new classes
3. **Monitor Accuracy:** Should reach 90%+ for good results

### Testing:
1. Test with real photos after training
2. Check if new weeds are detected correctly
3. Verify old weeds still work
4. Test "not_weed" still works

---

## Troubleshooting

### "Model accuracy is low"
- Add more images (aim for 500+ per class)
- Ensure images are clear and well-lit
- Balance dataset (similar counts per class)
- Train for more epochs (150-200)

### "New weed not detected"
- Check folder name matches weed_info.json
- Verify images are in correct folder
- Ensure images are JPG or PNG
- Retrain the model

### "Old weeds stopped working"
- Dataset might be imbalanced
- Add more images to old classes
- Retrain with more epochs

### "Training takes too long"
- Reduce batch size
- Use fewer epochs for testing
- Consider using GPU if available

---

## Current Dataset Status

After initial setup, you have:
- ✓ crabgrass: 927 images
- ✓ makahiya: 1,290 images
- ✓ morsikos: 1,044 images
- ✓ teki: 1,043 images
- ⚠ not_weed: 33 images (add more!)

**Recommendation:** Add more not_weed images first (aim for 200+)

---

## Checklist for Adding New Weed

- [ ] Create folder in `dataset/weeds/`
- [ ] Add 200+ images to folder
- [ ] Update `weed_info.json` with weed details
- [ ] Run `python train_model.py`
- [ ] Wait for training to complete
- [ ] Copy new model files to Android app
- [ ] Rebuild Android app
- [ ] Test new weed detection
- [ ] Test old weeds still work
- [ ] Test not_weed still works

---

## Quick Reference Commands

```bash
# Add new weed (interactive)
python add_new_weed_class.py

# Train model
python train_model.py

# Start admin panel
python unified_admin_server.py

# Copy model to app
copy models\weed_detector.tflite WeedDetectorApp\app\src\main\assets\
copy models\labels.txt WeedDetectorApp\app\src\main\assets\
copy weed_info.json WeedDetectorApp\app\src\main\assets\
```

---

## Example Workflow

1. **Identify new weed to add:** "Cogon Grass"
2. **Run script:** `python add_new_weed_class.py`
3. **Collect images:** Take 300 photos with phone
4. **Transfer images:** Copy to `dataset/weeds/cogon_grass/`
5. **Train model:** Use admin panel or terminal
6. **Update app:** Copy new model files
7. **Test:** Scan real cogon grass with app
8. **Success!** App now detects 6 weed types

---

**Ready to expand your model!** Use the script or follow the manual steps above.
