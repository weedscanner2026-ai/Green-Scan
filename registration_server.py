"""
User Registration Server for Green Scan App
Handles user registration, admin dashboard, and model training
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sqlite3
import hashlib
import secrets
from datetime import datetime
import os
import subprocess
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'admin_panel/dataset/weeds'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database setup
DB_PATH = 'users.db'

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

# API Routes for Mobile App

@app.route('/api/register', methods=['POST'])
def register_user():
    """Register a new user from mobile app"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['username', 'email', 'password', 'full_name', 'user_type']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if username or email exists
        c.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                 (data['username'], data['email']))
        if c.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'}), 400
        
        # Insert new user
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
        
        if user[3] == 0:  # is_active
            conn.close()
            return jsonify({'success': False, 'message': 'Account is deactivated'}), 403
        
        # Update last login
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
    
    # Get all users
    c.execute('''SELECT id, username, email, full_name, user_type, 
                institution, phone, registered_date, last_login, is_active
                FROM users ORDER BY registered_date DESC''')
    
    users = c.fetchall()
    
    # Get statistics
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
                          others=others)

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

if __name__ == '__main__':
    init_db()
    print("=" * 60)
    print("Green Scan REGISTRATION SERVER")
    print("=" * 60)
    print("\nDefault Admin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nAdmin Dashboard: http://localhost:5000/admin/login")
    print("API Endpoint: http://localhost:5000/api/")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
