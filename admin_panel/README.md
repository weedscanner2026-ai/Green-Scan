# Weed Detection Admin Panel

Professional web-based interface for managing datasets and training AI models.

## Features

- 📊 **Dataset Management**
  - View statistics (total images, classes, distribution)
  - Upload multiple images at once
  - Delete weed types
  - Real-time statistics updates

- 🤖 **Model Training**
  - Configure training parameters (epochs, batch size)
  - Real-time training progress monitoring
  - Live accuracy and loss metrics
  - Download trained model

- 🎨 **Professional UI**
  - Modern, responsive design
  - Easy to use for non-technical users
  - Real-time updates
  - Visual feedback

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

3. Open browser:
```
http://localhost:5000
```

## Usage

### Upload Images

1. Enter weed type name (e.g., "crabgrass", "teki")
2. Click "Select Images" and choose multiple photos
3. Click "Upload Images"
4. Statistics will update automatically

### Train Model

1. Check dataset statistics (recommended: 200+ images per weed)
2. Set training parameters:
   - Epochs: 50-100 (more = better but slower)
   - Batch Size: 16 (lower = more stable)
3. Click "Start Training"
4. Monitor progress in real-time
5. Download model when complete

### Download Model

1. After training completes
2. Click "Download Trained Model"
3. Model file: `weed_detector.tflite`
4. Copy to Android app assets folder

## API Endpoints

- `GET /` - Admin dashboard
- `GET /api/dataset/stats` - Get dataset statistics
- `POST /api/dataset/upload` - Upload images
- `DELETE /api/dataset/delete/<weed_type>` - Delete weed type
- `POST /api/train/start` - Start training
- `GET /api/train/status` - Get training status
- `GET /api/model/download` - Download trained model

## For Panel Presentation

This admin panel demonstrates:
- Professional software engineering practices
- Full-stack development (backend + frontend)
- Real-time monitoring and updates
- User-friendly interface for non-technical users
- Production-ready deployment

## Screenshots

The interface includes:
- Dashboard with statistics cards
- Upload section with drag-and-drop
- Training progress with live metrics
- Professional gradient design
- Responsive layout for all devices

## Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **ML**: TensorFlow/Keras
- **Design**: Modern Material Design principles
