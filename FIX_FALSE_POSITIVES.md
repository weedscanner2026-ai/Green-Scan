# Fix False Positives (Non-Weeds Detected as Weeds)

## Problem
The app detects non-weed objects (laptops, phones, etc.) as weeds because the model was only trained on weed images.

## Solution
Add a "not_weed" class to teach the model what is NOT a weed.

---

## Step 1: Add Non-Weed Images

You need to collect 200-300 images of things that are NOT weeds:

### What to Include:
- **Grass** (lawn grass, not weeds)
- **Flowers** (roses, sunflowers, orchids, etc.)
- **Crops** (rice plants, corn, vegetables)
- **Soil/Ground** (bare soil, rocks, pavement)
- **Common Objects** (phones, laptops, books, walls, furniture)
- **Hands/Body Parts** (people often accidentally scan themselves)

### Where to Get Images:
1. **Take your own photos** (recommended - most relevant)
   - Take 50-100 photos around your house/campus
   - Include: grass, flowers, objects, walls, etc.

2. **Download from free image sites:**
   - Unsplash.com
   - Pexels.com
   - Pixabay.com
   - Search: "grass", "flowers", "rice plant", "corn", "soil"

3. **Use the download script** (limited samples):
   ```
   python download_not_weed_images.py
   ```

### Save Images Here:
```
dataset/weeds/not_weed/
```

Put all non-weed images in this folder (already created).

---

## Step 2: Retrain the Model

Once you have 200+ images in `dataset/weeds/not_weed/`:

```bash
python train_model.py
```

This will:
- Include the new "not_weed" class
- Train the model to recognize 5 classes (4 weeds + not_weed)
- Generate new `weed_detector.tflite` and `labels.txt`

---

## Step 3: Update Android App

After retraining, copy the new model files to the app:

```bash
# Copy new model files
copy models\weed_detector.tflite WeedDetectorApp\app\src\main\assets\
copy models\labels.txt WeedDetectorApp\app\src\main\assets\
copy weed_info.json WeedDetectorApp\app\src\main\assets\
```

Then rebuild the app in Android Studio.

---

## Step 4: Test

Test the app with:
- ✓ Real weed images (should detect correctly)
- ✓ Laptop, phone, book (should show "Not a Weed")
- ✓ Grass, flowers (should show "Not a Weed")
- ✓ Random objects (should show "Not a Weed")

---

## Quick Start (Minimal Effort)

If you don't have time to collect 200+ images:

1. **Take 50 quick photos** with your phone:
   - 10 photos of grass
   - 10 photos of flowers
   - 10 photos of your laptop/phone/books
   - 10 photos of walls/furniture
   - 10 photos of soil/ground

2. Transfer to `dataset/weeds/not_weed/`

3. Retrain: `python train_model.py`

4. Copy new model to app

This minimal approach will help, but more images = better accuracy!

---

## Alternative: Increase Confidence Threshold

If you can't retrain right now, I've already increased the confidence threshold to 75%.

This means the app will show "UNCERTAIN DETECTION" for most non-weed objects.

To make it even stricter, edit `MainActivity.java`:
```java
float confidenceThreshold = 0.85f; // 85% minimum
```

But this is just a workaround - retraining with "not_weed" class is the proper solution.

---

## Current Status

✓ Created `dataset/weeds/not_weed/` folder
✓ Updated `weed_info.json` with "not_weed" class info
✓ Increased confidence threshold to 75%
✓ Created download script (optional)

⚠ **Next:** Add images to `dataset/weeds/not_weed/` and retrain!
