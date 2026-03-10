# Weed Detection Model Training

## Philippine Weeds Dataset

This project is configured for common Philippine weeds including:
- Crabgrass, Morsikos, Paragis, Teki, Makahiya, and more

See `weed_info.json` for complete list with scientific names and descriptions.

## Quick Start

1. **Create folder structure**:
```bash
python create_dataset_folders.py
```

2. **Collect images** (see `dataset_guide_philippines.md`):
   - 200+ images per weed type
   - Variety in angles, lighting, growth stages
   - Use your phone camera

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Validate dataset** (recommended):
```bash
python validate_dataset.py
```

5. **Train the model**:
```bash
python train_model.py
```

6. **Evaluate accuracy**:
```bash
python evaluate_model.py
```

7. **Test TFLite model**:
```bash
python test_tflite_model.py
```

8. **Deploy to Android**:
   - Copy `models/weed_detector.tflite` → `app/src/main/assets/`
   - Copy `models/labels.txt` → `app/src/main/assets/`
   - Copy `weed_info.json` → `app/src/main/assets/`
   - See `android/` folder for integration code

## Expected Results

With 200+ images per weed type, expect 90-95% accuracy.

## Files

- `train_model.py` - Training script with high accuracy settings
- `evaluate_model.py` - Model evaluation and metrics
- `validate_dataset.py` - Pre-training dataset validation
- `test_tflite_model.py` - Test TFLite model before deployment
- `weed_info.json` - Philippine weed database
- `dataset_guide_philippines.md` - Collection guide for Philippines
- `create_dataset_folders.py` - Auto-create folder structure
- `android/` - Android integration code
