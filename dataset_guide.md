# Weed Dataset Collection Guide

## Dataset Structure

Create your dataset folder with this structure (or run `python create_dataset_folders.py`):

```
dataset/
  weeds/
    crabgrass/
      img001.jpg
      img002.jpg
      ...
    morsikos/
      img001.jpg
      img002.jpg
      ...
    paragis/
      img001.jpg
      ...
    teki/
      img001.jpg
      ...
    makahiya/
      img001.jpg
      ...
    (add more weed types)
```

## Recommended Weed Types to Include

Based on common Philippine weeds:

1. crabgrass (Damong-alat)
2. morsikos (Spanish Needle)
3. paragis (Goosegrass)
4. teki (Nutsedge)
5. makahiya (Sensitive Plant)
6. kulitis (Slender Amaranth)
7. talahib (Wild Sugarcane)
8. damong-maria (Mugwort)
9. tawa-tawa (Hairy Spurge)
10. kangkong-aso (Wild Water Spinach)
11. ulasiman-bato (Tropical Chickweed)
12. alusiman (Purslane)
13. halamang-aso (Spider Flower)
14. sabila-sabila (Nodeweed)
15. botoncillo (Toothache Plant)

**For Philippine-specific guide, see: dataset_guide_philippines.md**

## Image Collection Guidelines for HIGH ACCURACY

### Minimum Images Per Weed Type
- **Minimum**: 100 images per weed type
- **Recommended**: 200-500 images per weed type
- **Optimal**: 500+ images per weed type

### Image Quality Requirements

1. **Resolution**: Minimum 640x480, recommended 1024x768 or higher
2. **Format**: JPG, JPEG, or PNG
3. **File size**: 100KB - 5MB per image

### Diversity Requirements (CRITICAL for accuracy)

Capture images with variety in:

#### 1. Growth Stages
- Seedling stage
- Young plant
- Mature plant
- Flowering stage
- Seed production stage

#### 2. Lighting Conditions
- Bright sunlight
- Overcast/cloudy
- Morning light
- Afternoon light
- Shade

#### 3. Angles & Distances
- Top-down view (bird's eye)
- 45-degree angle
- Side view
- Close-up (leaves/flowers)
- Medium distance (whole plant)
- Far distance (plant in context)

#### 4. Backgrounds
- Soil/dirt
- Grass/lawn
- Gravel
- Pavement/concrete
- Mulch
- Mixed vegetation

#### 5. Plant Conditions
- Healthy specimens
- Damaged/wilted
- Wet (after rain/dew)
- Dry
- Partially hidden by other plants

#### 6. Camera Variations
- Different phones/cameras
- Different focus levels
- Slight blur (realistic conditions)

## Where to Find Images

### Option 1: Take Your Own Photos (BEST)
- Walk around your area
- Visit parks, gardens, roadsides
- Take multiple photos of same plant from different angles
- Use your phone camera

### Option 2: Online Datasets
- iNaturalist (https://www.inaturalist.org)
- PlantNet (https://plantnet.org)
- Google Images (verify licensing)
- Kaggle datasets
- Agricultural research databases

### Option 3: Combine Both
- Use online images as base (50%)
- Add your own photos (50%)
- This gives best real-world accuracy

## Image Naming Convention

Use descriptive names:
```
dandelion_001.jpg
dandelion_002.jpg
crabgrass_closeup_001.jpg
crabgrass_flowering_001.jpg
```

## Data Augmentation (Automatic)

The training script automatically applies:
- Random horizontal flips
- Random rotations (±20%)
- Random zoom (±20%)
- Random contrast adjustments

This multiplies your effective dataset size!

## Quality Checks Before Training

1. **Balance**: Each weed type should have similar number of images
2. **Variety**: Check you have different angles, lighting, stages
3. **Accuracy**: Verify images are correctly labeled
4. **Remove**: Delete blurry, mislabeled, or duplicate images

## Expected Accuracy by Dataset Size

| Images per Class | Expected Accuracy |
|-----------------|-------------------|
| 50-100          | 70-80%           |
| 100-200         | 80-88%           |
| 200-500         | 88-94%           |
| 500+            | 94-98%           |

## Tips for Maximum Accuracy

1. **More variety > More quantity**: 200 diverse images beats 500 similar ones
2. **Real-world conditions**: Include challenging scenarios (partial occlusion, mixed plants)
3. **Consistent labeling**: Double-check folder names match weed_info.json
4. **Test set**: Keep 20% of images for validation (automatic in script)
5. **Regular updates**: Add new images and retrain periodically

## Quick Start Checklist

- [ ] Run: python create_dataset_folders.py (creates folder structure)
- [ ] Read dataset_guide_philippines.md for Philippine-specific tips
- [ ] Collect minimum 200 images per weed type
- [ ] Ensure variety in angles, lighting, stages
- [ ] Verify all images are correctly labeled
- [ ] Check folder names match weed_info.json entries
- [ ] Run training script: python train_model.py
- [ ] Evaluate accuracy: python evaluate_model.py
- [ ] Add more images if accuracy < 90%
- [ ] Retrain until satisfied

## Example Collection Session

For one weed type (e.g., dandelion):
1. Find 10-15 different dandelion plants
2. Take 10-20 photos of each plant:
   - 3-4 from different angles
   - 2-3 close-ups
   - 2-3 with different backgrounds
   - 2-3 in different lighting
3. Total: 100-300 images in 1-2 hours
4. Repeat for each weed type

Good luck with your dataset collection!
