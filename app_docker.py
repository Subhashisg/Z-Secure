from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
import cv2
import numpy as np
import hashlib
import base64
import uuid
from datetime import datetime, timedelta
import secrets
from PIL import Image
import io
import json
from functools import wraps

# Add src to path and import our custom modules
import sys
sys.path.insert(0, 'src')

# Use simplified version for Docker
try:
    from face_recognition_service import FaceRecognitionService
except ImportError:
    from face_recognition_service_simple import FaceRecognitionService

from zsecure_encryption import ZSecureEncryption
from image_processor import ImageProcessor
from database_manager import DatabaseManager
from src.session_manager import SessionManager

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize services
face_service = FaceRecognitionService()
encryption_service = ZSecureEncryption()
image_processor = ImageProcessor()
db_manager = DatabaseManager()
session_manager = SessionManager()

# Create necessary directories
for folder in [app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER'], 'face_data']:
    os.makedirs(folder, exist_ok=True)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            
            if not all([username, password, email]):
                flash('All fields are required', 'error')
                return redirect(url_for('register'))
            
            # Register user in database
            user_id = db_manager.create_user(username, password, email)
            if user_id:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Username may already exist.', 'error')
                
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db_manager.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_files = db_manager.get_user_files(session['user_id'])
    return render_template('dashboard.html', files=user_files)

@app.route('/face_auth')
@login_required
def face_auth():
    return render_template('face_auth.html')

@app.route('/api/face_auth', methods=['POST'])
@login_required
def api_face_auth():
    try:
        data = request.get_json()
        face_data = data.get('faceData')
        
        if not face_data:
            return jsonify({'success': False, 'message': 'No face data provided'})
        
        # Use simplified authentication
        result = face_service.authenticate_face_simple(face_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Authentication error: {str(e)}'})

@app.route('/manage_face')
@login_required
def manage_face():
    return render_template('manage_face.html')

@app.route('/api/register_face', methods=['POST'])
@login_required
def api_register_face():
    try:
        data = request.get_json()
        face_data = data.get('faceData')
        
        if not face_data:
            return jsonify({'success': False, 'message': 'No face data provided'})
        
        # Use simplified registration
        result = face_service.register_face_simple(session['user_id'], face_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration error: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
