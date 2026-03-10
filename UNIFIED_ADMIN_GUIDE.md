# Unified Admin Panel Guide

## Overview
The new unified admin panel combines user management and model training in one interface with a side navigation bar.

---

## Features

### 1. Side Navigation Bar
- **User Management** - View and manage registered users
- **Model Training** - Train the AI model with your dataset
- Easy switching between sections
- Admin info and logout button

### 2. User Management Page
- View all registered users
- User statistics (total, students, agriculturists, others)
- Activate/Deactivate user accounts
- Track registration dates and last login

### 3. Model Training Page
- View dataset statistics
- Configure training parameters (epochs, batch size)
- Start training with one click
- Real-time training progress
- Live metrics (accuracy, loss, epoch)
- Training log viewer

---

## Quick Start

### 1. Start the Unified Admin Server

```bash
python unified_admin_server.py
```

You should see:
```
UNIFIED Green Scan ADMIN SERVER
Default Admin Credentials:
  Username: admin
  Password: admin123

Admin Dashboard: http://localhost:5000/admin/login
```

### 2. Access Admin Panel

1. Open browser: `http://localhost:5000/admin/login`
2. Login with:
   - Username: `admin`
   - Password: `admin123`
3. You'll see the User Management page

### 3. Navigate Between Sections

Use the side navigation bar:
- Click **👥 User Management** to view users
- Click **🤖 Model Training** to train the model

---

## Using the Training Page

### View Dataset Statistics

The training page shows:
- Total images in dataset
- Images per class (crabgrass, makahiya, morsikos, teki, not_weed)

### Configure Training

1. **Number of Epochs:** How many times to train (default: 100)
   - More epochs = better accuracy (but takes longer)
   - Recommended: 50-150 epochs

2. **Batch Size:** Images processed at once (default: 16)
   - Larger = faster but needs more memory
   - Recommended: 16-32

### Start Training

1. Set your parameters
2. Click **"Start Training"** button
3. Watch the progress in real-time:
   - Progress bar shows completion %
   - Current epoch / total epochs
   - Accuracy and loss metrics
   - Training log at bottom

### Training Progress

The page updates every 2 seconds showing:
- **Status Message:** Current training status
- **Progress Bar:** Visual progress indicator
- **Epoch:** Current epoch number
- **Accuracy:** Model accuracy (higher is better)
- **Loss:** Training loss (lower is better)
- **Training Log:** Last 20 lines of output

### When Training Completes

- Progress bar reaches 100%
- Status shows "Training completed successfully!"
- Button becomes enabled again
- New model files saved in `models/` folder

---

## Training Tips

### For Best Results:

1. **Balanced Dataset:**
   - Each class should have similar number of images
   - Minimum 200 images per class recommended
   - Currently not_weed has only 33 images (add more!)

2. **Training Parameters:**
   - Start with 50 epochs for testing
   - Use 100-150 epochs for final model
   - Batch size 16 works well for most systems

3. **Monitor Progress:**
   - Accuracy should increase over time
   - Loss should decrease over time
   - If accuracy stops improving, training is done

4. **After Training:**
   - Copy new model to Android app:
     ```
     copy models\weed_detector.tflite WeedDetectorApp\app\src\main\assets\
     copy models\labels.txt WeedDetectorApp\app\src\main\assets\
     ```
   - Rebuild Android app

---

## File Structure

```
weeAdmin/
├── unified_admin_server.py      # Main server
├── admin_templates/              # Admin HTML templates
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── admin_training.html
├── static/
│   └── admin_style.css          # Admin panel styles
├── dataset/weeds/               # Training images
│   ├── crabgrass/
│   ├── makahiya/
│   ├── morsikos/
│   ├── teki/
│   └── not_weed/
└── models/                      # Trained models
    ├── weed_detector.tflite
    ├── labels.txt
    └── best_model.h5
```

---

## API Endpoints

### Mobile App APIs
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Admin APIs
- `GET /admin/dashboard` - User management page
- `GET /admin/training` - Model training page
- `POST /admin/train/start` - Start training
- `GET /admin/train/status` - Get training status
- `GET /admin/dataset/stats` - Get dataset statistics
- `POST /admin/user/<id>/toggle` - Toggle user status

---

## Troubleshooting

### Training doesn't start:
- Check if `train_model.py` exists
- Verify dataset folder has images
- Check Python is in PATH

### Progress not updating:
- Refresh the page
- Check browser console for errors
- Verify server is running

### Training fails:
- Check training log for errors
- Verify TensorFlow is installed
- Check dataset has valid images

### Can't access admin panel:
- Verify server is running
- Check URL: http://localhost:5000/admin/login
- Clear browser cache

---

## Comparison: Old vs New

### Old System:
- ❌ Separate servers for users and training
- ❌ No navigation between sections
- ❌ Terminal-based training only
- ❌ No real-time progress

### New Unified System:
- ✓ Single server for everything
- ✓ Side navigation bar
- ✓ Web-based training interface
- ✓ Real-time progress updates
- ✓ Training log viewer
- ✓ Better user experience

---

## Next Steps

1. **Start the unified server:**
   ```bash
   python unified_admin_server.py
   ```

2. **Login to admin panel:**
   - http://localhost:5000/admin/login

3. **Add more not_weed images:**
   - Take photos of grass, flowers, objects
   - Put in `dataset/weeds/not_weed/`

4. **Train the model:**
   - Go to Model Training page
   - Set epochs to 100
   - Click Start Training
   - Wait for completion

5. **Update Android app:**
   - Copy new model files
   - Rebuild app
   - Test on phone

---

## Success Indicators

✓ Server starts without errors
✓ Admin login works
✓ Can switch between User Management and Training pages
✓ Dataset statistics show correct counts
✓ Training starts when button clicked
✓ Progress updates in real-time
✓ Training completes successfully
✓ New model files created

---

## Benefits

1. **Unified Interface** - Everything in one place
2. **Easy Navigation** - Side bar for quick switching
3. **Real-time Monitoring** - Watch training progress live
4. **Better UX** - Professional admin panel design
5. **No Terminal Needed** - All through web interface
6. **Training Logs** - See what's happening
7. **Mobile + Desktop** - Manage users and train models

---

**Ready to use!** Start the server and access the admin panel.
