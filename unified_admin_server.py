"""
Unified Admin Server for Green Scan App
Handles user registration, user management, and model training
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
from datetime import datetime
import os
import subprocess
import threading
import json
from pathlib import Path

app = Flask(__name__, template_folder='admin_templates')
app.secret_key = secrets.token_hex(32)
CORS(app)

# Database setup
DB_PATH = 'users.db'

# Training status
training_status = {
    'is_training': False,
    'progress': 0,
    'current_epoch': 0,
    'total_epochs': 0,
    'accuracy': 0,
    'loss': 0,
    'message': 'Ready to train',
    'log': []
}

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        user_type TEXT NOT NULL,
        institution TEXT,
        phone TEXT,
        registered_date TEXT NOT NULL,
        last_login TEXT,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Admin table
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )''')
    
    # Create default admin if not exists
    admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        c.execute('INSERT INTO admins (username, password_hash) VALUES (?, ?)', 
                 ('admin', admin_pass))
    except:
        pass
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_dataset_stats():
    """Get dataset statistics"""
    dataset_path = Path('dataset/weeds')
    stats = {}
    total = 0
    
    if dataset_path.exists():
        for class_dir in dataset_path.iterdir():
            if class_dir.is_dir():
                count = len(list(class_dir.glob('*.jpg'))) + len(list(class_dir.glob('*.png')))
                stats[class_dir.name] = count
                total += count
    
    return stats, total

# API Routes for Mobile App

@app.route('/api/register', methods=['POST'])
def register_user():
    """Register a new user from mobile app"""
    try:
        data = request.json
        
        required = ['username', 'email', 'password', 'full_name', 'user_type']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                 (data['username'], data['email']))
        if c.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'}), 400
        
        password_hash = hash_password(data['password'])
        registered_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('''INSERT INTO users 
                    (username, email, password_hash, full_name, user_type, 
                     institution, phone, registered_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (data['username'], data['email'], password_hash, 
                  data['full_name'], data['user_type'],
                  data.get('institution', ''), data.get('phone', ''),
                  registered_date))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Registration successful',
            'username': data['username']
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login_user():
    """Login user from mobile app"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        password_hash = hash_password(password)
        c.execute('''SELECT id, full_name, user_type, is_active 
                    FROM users 
                    WHERE username = ? AND password_hash = ?''',
                 (username, password_hash))
        
        user = c.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        if user[3] == 0:
            conn.close()
            return jsonify({'success': False, 'message': 'Account is deactivated'}), 403
        
        last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('UPDATE users SET last_login = ? WHERE id = ?', (last_login, user[0]))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user[0],
                'full_name': user[1],
                'user_type': user[2]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Admin Web Dashboard Routes

@app.route('/')
def index():
    """Redirect to admin login"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        password_hash = hash_password(password)
        c.execute('SELECT id FROM admins WHERE username = ? AND password_hash = ?',
                 (username, password_hash))
        
        admin = c.fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard - view all users"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''SELECT id, username, email, full_name, user_type, 
                institution, phone, registered_date, last_login, is_active
                FROM users ORDER BY registered_date DESC''')
    users = c.fetchall()
    
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE user_type = "Student"')
    students = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE user_type = "Agriculturist"')
    agriculturists = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE user_type = "Other"')
    others = c.fetchone()[0]
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                          users=users,
                          total_users=total_users,
                          students=students,
                          agriculturists=agriculturists,
                          others=others,
                          active_page='users')

@app.route('/admin/training')
def admin_training():
    """Admin training page"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    dataset_stats, total_images = get_dataset_stats()
    
    return render_template('admin_training.html',
                          dataset_stats=dataset_stats,
                          total_images=total_images,
                          training_status=training_status,
                          active_page='training')

@app.route('/admin/reports')
def admin_reports():
    """Admin reports and analytics page"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get user statistics
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE user_type = "Student"')
    students = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE user_type = "Agriculturist"')
    agriculturists = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE user_type = "Other"')
    others = c.fetchone()[0]
    
    # Get active vs inactive users
    c.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
    active_users = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE is_active = 0')
    inactive_users = c.fetchone()[0]
    
    # Get registrations by date (last 30 days)
    c.execute('''SELECT DATE(registered_date) as date, COUNT(*) as count 
                FROM users 
                WHERE registered_date >= date('now', '-30 days')
                GROUP BY DATE(registered_date)
                ORDER BY date''')
    registrations_by_date = c.fetchall()
    
    # Get registrations by month (last 12 months)
    c.execute('''SELECT strftime('%Y-%m', registered_date) as month, COUNT(*) as count 
                FROM users 
                WHERE registered_date >= date('now', '-12 months')
                GROUP BY strftime('%Y-%m', registered_date)
                ORDER BY month''')
    registrations_by_month = c.fetchall()
    
    # Get users with institutions
    c.execute('SELECT COUNT(*) FROM users WHERE institution IS NOT NULL AND institution != ""')
    users_with_institution = c.fetchone()[0]
    
    # Get top institutions
    c.execute('''SELECT institution, COUNT(*) as count 
                FROM users 
                WHERE institution IS NOT NULL AND institution != ""
                GROUP BY institution 
                ORDER BY count DESC 
                LIMIT 10''')
    top_institutions = c.fetchall()
    
    # Get login activity (users who logged in last 7 days)
    c.execute('''SELECT COUNT(*) FROM users 
                WHERE last_login >= date('now', '-7 days')''')
    active_last_week = c.fetchone()[0]
    
    conn.close()
    
    return render_template('admin_reports.html',
                          total_users=total_users,
                          students=students,
                          agriculturists=agriculturists,
                          others=others,
                          active_users=active_users,
                          inactive_users=inactive_users,
                          registrations_by_date=registrations_by_date,
                          registrations_by_month=registrations_by_month,
                          users_with_institution=users_with_institution,
                          top_institutions=top_institutions,
                          active_last_week=active_last_week,
                          active_page='reports')

@app.route('/admin/user/<int:user_id>/toggle', methods=['POST'])
def toggle_user_status(user_id):
    """Toggle user active status"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False}), 401
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('UPDATE users SET is_active = NOT is_active WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/admin/train/start', methods=['POST'])
def start_training():
    """Start model training"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    if training_status['is_training']:
        return jsonify({'success': False, 'message': 'Training already in progress'}), 400
    
    data = request.json
    epochs = data.get('epochs', 100)
    batch_size = data.get('batch_size', 16)
    
    def run_training():
        global training_status
        training_status['is_training'] = True
        training_status['message'] = 'Starting training...'
        training_status['total_epochs'] = epochs
        training_status['log'] = []
        
        try:
            # Run training script
            process = subprocess.Popen(
                ['python', 'train_model.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            for line in process.stdout:
                training_status['log'].append(line.strip())
                if 'Epoch' in line:
                    try:
                        parts = line.split('/')
                        if len(parts) >= 2:
                            current = int(parts[0].split()[-1])
                            training_status['current_epoch'] = current
                            training_status['progress'] = int((current / epochs) * 100)
                    except:
                        pass
                
                if 'accuracy:' in line:
                    try:
                        acc = float(line.split('accuracy:')[1].split()[0])
                        training_status['accuracy'] = acc
                    except:
                        pass
                
                if 'loss:' in line:
                    try:
                        loss = float(line.split('loss:')[1].split()[0])
                        training_status['loss'] = loss
                    except:
                        pass
            
            process.wait()
            
            if process.returncode == 0:
                training_status['message'] = 'Training completed successfully!'
                training_status['progress'] = 100
            else:
                training_status['message'] = 'Training failed!'
                
        except Exception as e:
            training_status['message'] = f'Error: {str(e)}'
        
        training_status['is_training'] = False
    
    thread = threading.Thread(target=run_training)
    thread.start()
    
    return jsonify({'success': True, 'message': 'Training started'})

@app.route('/admin/train/status')
def training_status_api():
    """Get training status"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False}), 401
    
    return jsonify(training_status)

@app.route('/admin/dataset/stats')
def dataset_stats_api():
    """Get dataset statistics"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False}), 401
    
    stats, total = get_dataset_stats()
    return jsonify({'stats': stats, 'total': total})

# ============================================================================
# MODEL UPDATE API ENDPOINTS (for Android app)
# ============================================================================

MODEL_VERSION_FILE = 'model_version.json'

def get_model_version():
    """Get current model version"""
    if os.path.exists(MODEL_VERSION_FILE):
        with open(MODEL_VERSION_FILE, 'r') as f:
            data = json.load(f)
            return data.get('version', 1)
    return 1

def set_model_version(version):
    """Set model version"""
    with open(MODEL_VERSION_FILE, 'w') as f:
        json.dump({
            'version': version,
            'updated_at': datetime.now().isoformat(),
            'weed_types': len([d for d in os.listdir('dataset/weeds') if os.path.isdir(os.path.join('dataset/weeds', d))])
        }, f, indent=2)

@app.route('/model/version', methods=['GET'])
def model_version():
    """Get current model version info"""
    version = get_model_version()
    weed_count = 0
    if os.path.exists('dataset/weeds'):
        weed_count = len([d for d in os.listdir('dataset/weeds') if os.path.isdir(os.path.join('dataset/weeds', d))])
    
    return jsonify({
        'version': version,
        'weed_types': weed_count,
        'updated_at': datetime.now().isoformat()
    })

@app.route('/model/download/model', methods=['GET'])
def download_model():
    """Download the latest model file"""
    model_path = 'models/weed_detector.tflite'
    if os.path.exists(model_path):
        from flask import send_file
        return send_file(model_path, as_attachment=True, download_name='weed_detector.tflite')
    return jsonify({'error': 'Model not found'}), 404

@app.route('/model/download/labels', methods=['GET'])
def download_labels():
    """Download the latest labels file"""
    labels_path = 'models/labels.txt'
    if os.path.exists(labels_path):
        from flask import send_file
        return send_file(labels_path, as_attachment=True, download_name='labels.txt')
    return jsonify({'error': 'Labels not found'}), 404

@app.route('/model/download/info', methods=['GET'])
def download_info():
    """Download the latest weed info file"""
    info_path = 'weed_info.json'
    if os.path.exists(info_path):
        from flask import send_file
        return send_file(info_path, as_attachment=True, download_name='weed_info.json')
    return jsonify({'error': 'Weed info not found'}), 404

@app.route('/admin/model/publish', methods=['POST'])
def publish_model():
    """Increment model version to notify apps of update AND copy to Android assets"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Increment version
        current_version = get_model_version()
        new_version = current_version + 1
        set_model_version(new_version)
        
        # Copy files to Android assets
        android_assets = 'WeedDetectorApp/app/src/main/assets'
        if os.path.exists('WeedDetectorApp'):
            try:
                os.makedirs(android_assets, exist_ok=True)
                
                import shutil
                # Copy model
                shutil.copy2('models/weed_detector.tflite', 
                           os.path.join(android_assets, 'weed_detector.tflite'))
                # Copy labels
                shutil.copy2('models/labels.txt', 
                           os.path.join(android_assets, 'labels.txt'))
                # Copy weed info
                shutil.copy2('weed_info.json', 
                           os.path.join(android_assets, 'weed_info.json'))
                
                return jsonify({
                    'success': True,
                    'message': f'Model published as version {new_version}',
                    'version': new_version,
                    'android_updated': True,
                    'note': 'Files copied to Android assets. Rebuild the APK in Android Studio.'
                })
            except Exception as e:
                return jsonify({
                    'success': True,
                    'message': f'Model published as version {new_version}',
                    'version': new_version,
                    'android_updated': False,
                    'warning': f'Could not copy to Android assets: {str(e)}'
                })
        else:
            return jsonify({
                'success': True,
                'message': f'Model published as version {new_version}',
                'version': new_version,
                'android_updated': False,
                'note': 'WeedDetectorApp folder not found'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error publishing model: {str(e)}'
        })

# ============================================================================
# DATASET MANAGEMENT ROUTES
# ============================================================================

@app.route('/admin/dataset')
def admin_dataset():
    """Dataset management page"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    stats, total = get_dataset_stats()
    return render_template('admin_dataset.html', dataset_stats={'stats': stats, 'total': total})

@app.route('/admin/dataset/add', methods=['POST'])
def add_weed_class():
    """Add new weed class via web form"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        weed_name = data.get('weed_name', '').strip().lower()
        
        # Validate weed name
        if not weed_name:
            return jsonify({'success': False, 'message': 'Weed name is required'})
        
        if not weed_name.replace('_', '').isalpha():
            return jsonify({'success': False, 'message': 'Weed name must contain only letters and underscores'})
        
        # Create folder
        folder_path = os.path.join('dataset', 'weeds', weed_name)
        if os.path.exists(folder_path):
            return jsonify({'success': False, 'message': f'Weed class "{weed_name}" already exists'})
        
        os.makedirs(folder_path, exist_ok=True)
        
        # Update weed_info.json
        weed_info_path = 'weed_info.json'
        if os.path.exists(weed_info_path):
            with open(weed_info_path, 'r') as f:
                weed_info = json.load(f)
        else:
            weed_info = {'weeds': {}}
        
        # Add new weed info
        weed_info['weeds'][weed_name] = {
            'scientific_name': data.get('scientific_name', 'N/A'),
            'family': data.get('family', 'N/A'),
            'description': data.get('description', 'No description available'),
            'identification': data.get('identification', 'N/A'),
            'habitat': data.get('habitat', 'N/A'),
            'control_methods': data.get('control_methods', 'N/A'),
            'toxicity': data.get('toxicity', 'Unknown'),
            'growth_season': data.get('growth_season', 'N/A')
        }
        
        # Save updated weed_info.json
        with open(weed_info_path, 'w') as f:
            json.dump(weed_info, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Weed class "{weed_name}" created successfully!',
            'folder_path': folder_path
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/dataset/open-folder', methods=['POST'])
def open_folder():
    """Open dataset folder in file explorer"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        weed_name = data.get('weed_name', '')
        folder_path = os.path.join('dataset', 'weeds', weed_name)
        
        if not os.path.exists(folder_path):
            return jsonify({'success': False, 'message': 'Folder not found'})
        
        # Open folder in file explorer (Windows)
        import subprocess
        subprocess.Popen(f'explorer "{os.path.abspath(folder_path)}"')
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    init_db()
    
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("GREEN SCAN ADMIN SERVER")
    print("=" * 60)
    print("\nDefault Admin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print(f"\nServer running on port: {port}")
    print(f"Debug mode: {debug}")
    print("=" * 60)
    
    app.run(host=host, port=port, debug=debug)
