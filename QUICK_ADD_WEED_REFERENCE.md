# Quick Reference: Adding New Weeds

## 🚀 Super Quick Method (3 Steps)

### 1. Run Script
```bash
python add_new_weed_class.py
```

### 2. Add Images
Put 200+ images in the created folder

### 3. Train
```bash
python train_model.py
```

Done! 🎉

---

## 📋 Manual Method (5 Steps)

### 1. Create Folder
```bash
mkdir dataset\weeds\new_weed_name
```

### 2. Add Images
Copy 200+ images to the folder

### 3. Update weed_info.json
Add weed information to the JSON file

### 4. Train Model
```bash
python train_model.py
```

### 5. Update App
```bash
copy models\weed_detector.tflite WeedDetectorApp\app\src\main\assets\
copy models\labels.txt WeedDetectorApp\app\src\main\assets\
copy weed_info.json WeedDetectorApp\app\src\main\assets\
```

---

## 🌐 Using Admin Panel

### 1. Add Folder & Images Manually
```
dataset/weeds/new_weed_name/
└── (your images)
```

### 2. Update weed_info.json

### 3. Start Admin Server
```bash
python unified_admin_server.py
```

### 4. Train via Web
- Go to: http://localhost:5000/admin/login
- Click "Model Training"
- Click "Start Training"
- Watch progress!

---

## 📸 Image Requirements

| Requirement | Value |
|------------|-------|
| **Minimum** | 200 images |
| **Recommended** | 500 images |
| **Optimal** | 1000+ images |
| **Format** | JPG or PNG |
| **Quality** | Clear, well-lit |

---

## 📁 Folder Naming

✓ **Good:** `cogon_grass`, `water_hyacinth`
✗ **Bad:** `Cogon Grass`, `cogon-grass`

**Rules:**
- Lowercase only
- Underscores for spaces
- No special characters

---

## 🔄 Complete Workflow

```
Create Folder → Add Images → Update Info → Train → Copy to App → Rebuild → Test
```

---

## 💡 Tips

1. **Balance Dataset:** Similar image counts per class
2. **Variety:** Different angles, lighting, growth stages
3. **Quality:** Clear, focused, well-lit photos
4. **Test:** Always test after retraining

---

## 🛠️ Useful Commands

```bash
# Add new weed (interactive)
python add_new_weed_class.py

# Train model (terminal)
python train_model.py

# Train model (web interface)
python unified_admin_server.py

# View dataset
dir dataset\weeds

# Count images
dir dataset\weeds\weed_name | measure-object
```

---

## 📊 Current Dataset

```
crabgrass:    927 images ✓
makahiya:   1,290 images ✓
morsikos:   1,044 images ✓
teki:       1,043 images ✓
not_weed:      33 images ⚠ (add more!)
```

---

## ❓ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Low accuracy | Add more images (500+ per class) |
| Weed not detected | Check folder name, retrain |
| Training fails | Check Python/TensorFlow installed |
| Old weeds broken | Balance dataset, retrain |

---

## 📚 Full Guides

- **Detailed Guide:** `HOW_TO_ADD_NEW_WEEDS.md`
- **Structure Guide:** `DATASET_STRUCTURE_GUIDE.md`
- **Admin Panel:** `UNIFIED_ADMIN_GUIDE.md`

---

**Need help?** Check the full guides above! 🌿
