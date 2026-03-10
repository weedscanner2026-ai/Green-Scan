"""
Admin Panel for Weed Detection Model Training
Web-based interface for dataset management and model training
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import shutil
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'dataset/weeds'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variable to track training status
training_status = {
    'is_training': False,
    'progress': 0,
    'current_epoch': 0,
    'total_epochs': 0,
    'accuracy': 0,
    'loss': 0,
    'message': 'Ready to train'
}

@app.route('/')
def index():
    """Main admin dashboard"""
    return render_template('index.html')

@app.route('/api/dataset/stats')
def get_dataset_stats():
    """Get statistics about the current dataset"""
    stats = {}
    total_images = 0
    
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for weed_type in os.listdir(app.config['UPLOAD_FOLDER']):
            weed_path = os.path.join(app.config['UPLOAD_FOLDER'], weed_type)
            if os.path.isdir(weed_path):
                images = [f for f in os.listdir(weed_path) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                count = len(images)
                stats[weed_type] = count
                total_images += count
    
    return jsonify({
        'weed_types': stats,
        'total_images': total_images,
        'total_classes': len(stats)
    })

@app.route('/api/dataset/upload', methods=['POST'])
def upload_images():
    """Upload images for a specific weed type"""
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    weed_type = request.form.get('weed_type', '').strip().lower()
    if not weed_type:
        return jsonify({'error': 'Weed type is required'}), 400
    
    # Create directory if it doesn't exist
    weed_dir = os.path.join(app.config['UPLOAD_FOLDER'], weed_type)
    os.makedirs(weed_dir, exist_ok=True)
    
    files = request.files.getlist('files[]')
    uploaded_count = 0
    
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            # Add timestamp to avoid duplicates
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
            file.save(os.path.join(weed_dir, filename))
            uploaded_count += 1
    
    return jsonify({
        'success': True,
        'uploaded': uploaded_count,
        'weed_type': weed_type
    })

@app.route('/api/dataset/delete/<weed_type>', methods=['DELETE'])
def delete_weed_type(weed_type):
    """Delete all images for a specific weed type"""
    weed_dir = os.path.join(app.config['UPLOAD_FOLDER'], weed_type)
    
    if os.path.exists(weed_dir):
        shutil.rmtree(weed_dir)
        return jsonify({'success': True, 'message': f'Deleted {weed_type}'})
    
    return jsonify({'error': 'Weed type not found'}), 404

@app.route('/api/train/start', methods=['POST'])
def start_training():
    """Start model training in background"""
    global training_status
    
    if training_status['is_training']:
        return jsonify({'error': 'Training already in progress'}), 400
    
    # Get training parameters
    epochs = request.json.get('epochs', 50)
    batch_size = request.json.get('batch_size', 16)
    
    # Start training in background thread
    training_thread = threading.Thread(
        target=run_training,
        args=(epochs, batch_size)
    )
    training_thread.daemon = True
    training_thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Training started',
        'epochs': epochs,
        'batch_size': batch_size
    })

@app.route('/api/train/status')
def get_training_status():
    """Get current training status"""
    return jsonify(training_status)

@app.route('/api/model/download')
def download_model():
    """Download the trained model"""
    model_path = 'models/weed_detector.tflite'
    
    if os.path.exists(model_path):
        return send_file(model_path, as_attachment=True)
    
    return jsonify({'error': 'Model not found'}), 404

@app.route('/api/validate')
def validate_dataset():
    """Validate dataset before training"""
    import sys
    sys.path.append('..')
    from validate_dataset import validate_dataset
    
    # Capture validation output
    result = validate_dataset('dataset/weeds')
    
    return jsonify({
        'valid': result,
        'message': 'Dataset validation complete'
    })

def run_training(epochs, batch_size):
    """Run training process (called in background thread)"""
    global training_status
    
    training_status['is_training'] = True
    training_status['total_epochs'] = epochs
    training_status['message'] = 'Initializing training...'
    
    try:
        import sys
        sys.path.append('..')
        from train_model import train_and_save_model
        
        # Custom callback to update status
        class StatusCallback:
            def on_epoch_end(self, epoch, logs=None):
                training_status['current_epoch'] = epoch + 1
                training_status['progress'] = int((epoch + 1) / epochs * 100)
                training_status['accuracy'] = logs.get('accuracy', 0) * 100
                training_status['loss'] = logs.get('loss', 0)
                training_status['message'] = f'Training epoch {epoch + 1}/{epochs}'
        
        training_status['message'] = 'Training model...'
        train_and_save_model('dataset/weeds')
        
        training_status['is_training'] = False
        training_status['progress'] = 100
        training_status['message'] = 'Training complete!'
        
    except Exception as e:
        training_status['is_training'] = False
        training_status['message'] = f'Training failed: {str(e)}'
        print(f"Training error: {e}")

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('dataset/weeds', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    print("="*60)
    print("Weed Detection Admin Panel")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
