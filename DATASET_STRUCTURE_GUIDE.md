# Dataset Structure Guide

## Current Dataset Structure

```
weeAdmin/
│
├── dataset/
│   └── weeds/
│       ├── crabgrass/              ← Weed Class 1
│       │   ├── crab_001.jpg
│       │   ├── crab_002.jpg
│       │   ├── crab_003.jpg
│       │   └── ... (927 images total)
│       │
│       ├── makahiya/               ← Weed Class 2
│       │   ├── maka_001.jpg
│       │   ├── maka_002.jpg
│       │   └── ... (1,290 images total)
│       │
│       ├── morsikos/               ← Weed Class 3
│       │   ├── mors_001.jpg
│       │   ├── mors_002.jpg
│       │   └── ... (1,044 images total)
│       │
│       ├── teki/                   ← Weed Class 4
│       │   ├── teki_001.jpg
│       │   ├── teki_002.jpg
│       │   └── ... (1,043 images total)
│       │
│       └── not_weed/               ← Weed Class 5 (Non-weeds)
│           ├── grass_01.jpg
│           ├── flower_01.jpg
│           ├── laptop_01.jpg
│           └── ... (33 images total)
│
├── weed_info.json                  ← Information about all weeds
├── train_model.py                  ← Training script
└── add_new_weed_class.py          ← Script to add new weeds
```

---

## Adding a New Weed (Example: Cogon Grass)

### Step 1: Create New Folder

```
dataset/weeds/
├── crabgrass/
├── makahiya/
├── morsikos/
├── teki/
├── not_weed/
└── cogon_grass/        ← NEW FOLDER (create this)
```

### Step 2: Add Images

```
dataset/weeds/cogon_grass/
├── cogon_001.jpg       ← Add your images here
├── cogon_002.jpg
├── cogon_003.jpg
├── cogon_004.jpg
└── ... (add 200-1000 images)
```

### Step 3: After Training

The model will now detect 6 classes:
1. crabgrass
2. makahiya
3. morsikos
4. teki
5. not_weed
6. cogon_grass ← NEW!

---

## Adding Multiple Weeds

### Example: Adding 3 New Weeds

```
dataset/weeds/
├── crabgrass/          (existing)
├── makahiya/           (existing)
├── morsikos/           (existing)
├── teki/               (existing)
├── not_weed/           (existing)
├── cogon_grass/        ← NEW 1
│   └── (200+ images)
├── water_hyacinth/     ← NEW 2
│   └── (200+ images)
└── lantana/            ← NEW 3
    └── (200+ images)
```

After training, model detects 8 classes!

---

## Folder Naming Rules

### ✓ Good Names:
- `cogon_grass`
- `water_hyacinth`
- `madre_de_cacao`
- `purple_nutsedge`
- `hairy_beggarticks`

### ✗ Bad Names:
- `Cogon Grass` (has space)
- `cogon-grass` (has hyphen)
- `Cogon_Grass` (has uppercase)
- `cogon grass!` (has special character)

### Naming Convention:
1. All lowercase
2. Use underscores for spaces
3. No special characters
4. No numbers at start
5. Descriptive and clear

---

## Image Organization Tips

### Option 1: Simple Numbering
```
cogon_grass/
├── 001.jpg
├── 002.jpg
├── 003.jpg
└── ...
```

### Option 2: Descriptive Names
```
cogon_grass/
├── cogon_young_plant.jpg
├── cogon_mature_plant.jpg
├── cogon_flower_spike.jpg
├── cogon_leaves_closeup.jpg
└── ...
```

### Option 3: By Source
```
cogon_grass/
├── field_001.jpg
├── field_002.jpg
├── roadside_001.jpg
├── roadside_002.jpg
└── ...
```

All methods work! Choose what's easiest for you.

---

## Complete Project Structure

```
weeAdmin/
│
├── dataset/                        ← Training images
│   └── weeds/
│       ├── crabgrass/
│       ├── makahiya/
│       ├── morsikos/
│       ├── teki/
│       ├── not_weed/
│       └── [new_weed_folders]/
│
├── models/                         ← Trained models
│   ├── weed_detector.tflite      ← For Android app
│   ├── labels.txt                 ← Class names
│   └── best_model.h5              ← Full model
│
├── WeedDetectorApp/               ← Android app
│   └── app/src/main/assets/
│       ├── weed_detector.tflite  ← Copy from models/
│       ├── labels.txt             ← Copy from models/
│       └── weed_info.json         ← Copy from root
│
├── admin_templates/               ← Admin panel HTML
├── static/                        ← Admin panel CSS
├── templates/                     ← Old templates
│
├── weed_info.json                ← Weed information database
├── train_model.py                ← Training script
├── add_new_weed_class.py        ← Add new weed helper
├── unified_admin_server.py      ← Admin panel server
└── users.db                      ← User database
```

---

## Workflow Diagram

```
1. CREATE FOLDER
   dataset/weeds/new_weed/
          ↓
2. ADD IMAGES
   (200-1000 images)
          ↓
3. UPDATE INFO
   weed_info.json
          ↓
4. TRAIN MODEL
   python train_model.py
          ↓
5. NEW MODEL CREATED
   models/weed_detector.tflite
          ↓
6. COPY TO APP
   WeedDetectorApp/app/src/main/assets/
          ↓
7. REBUILD APP
   Android Studio
          ↓
8. TEST NEW WEED
   Scan with phone!
```

---

## Dataset Size Recommendations

### Minimum (for testing):
- 100 images per class
- Total: 500 images (5 classes)
- Training time: ~10 minutes
- Accuracy: ~80-85%

### Recommended (for production):
- 500 images per class
- Total: 2,500 images (5 classes)
- Training time: ~30 minutes
- Accuracy: ~90-95%

### Optimal (for best results):
- 1,000+ images per class
- Total: 5,000+ images (5 classes)
- Training time: ~60 minutes
- Accuracy: ~95-98%

---

## Current Status

Your current dataset:
```
Total Images: 4,337
Classes: 5

Distribution:
├── crabgrass:    927 images (21.4%) ✓ Good
├── makahiya:   1,290 images (29.8%) ✓ Good
├── morsikos:   1,044 images (24.1%) ✓ Good
├── teki:       1,043 images (24.1%) ✓ Good
└── not_weed:      33 images (0.8%)  ⚠ Need more!
```

**Recommendation:** Add 200+ more not_weed images for better balance.

---

## Quick Commands

```bash
# View dataset structure
dir dataset\weeds

# Count images in a folder
dir dataset\weeds\crabgrass | measure-object

# Create new weed folder
mkdir dataset\weeds\new_weed_name

# Add new weed with script
python add_new_weed_class.py

# Train model
python train_model.py

# View training results
dir models
```

---

## FAQs

**Q: Can I have different number of images per class?**
A: Yes, but try to keep them balanced (within 2x of each other).

**Q: What if I only have 50 images?**
A: Start with 50, but add more later and retrain for better accuracy.

**Q: Can I add images while training?**
A: No, add images first, then train. Don't modify during training.

**Q: Do I need to retrain from scratch?**
A: Yes, when adding new classes, retrain the entire model.

**Q: Can I remove a weed class?**
A: Yes, delete the folder and retrain. Update weed_info.json too.

**Q: How long does training take?**
A: Depends on dataset size and computer. Usually 20-60 minutes.

---

**Ready to expand your dataset!** Follow the structure above and use the helper scripts.
