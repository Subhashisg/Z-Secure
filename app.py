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

from face_recognition_service import FaceRecognitionService
from zsecure_encryption import ZSecureEncryption
from image_processor import ImageProcessor
from database_manager import DatabaseManager
from session_manager import SessionManager

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SESSION_TIMEOUT'] = 900  # 15 minutes session timeout

# Initialize services
face_service = FaceRecognitionService()
zsecure = ZSecureEncryption()
image_processor = ImageProcessor()
db_manager = DatabaseManager()
session_manager = SessionManager()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('face_data', exist_ok=True)

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Check session timeout
        if not session_manager.is_session_valid(session.get('session_id')):
            session.clear()
            flash('Session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        
        # Update session activity
        session_manager.update_session_activity(session.get('session_id'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session and session_manager.is_session_valid(session.get('session_id')):
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with facial ID capture"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not email or not password or not confirm_password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if db_manager.user_exists(email):
            flash('User with this email already exists', 'error')
            return render_template('register.html')
        
        return render_template('capture_face.html', email=email, password=password)
    
    return render_template('register.html')

@app.route('/capture_face', methods=['POST'])
def capture_face():
    """Capture and process facial data during registration"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        face_data = request.form.get('face_data')  # Base64 encoded image
        
        if not face_data:
            return jsonify({'success': False, 'message': 'No facial data received'})
        
        # Process facial data
        face_encoding = face_service.process_face_data(face_data)
        if face_encoding is None:
            return jsonify({'success': False, 'message': 'Could not detect face. Please try again.'})
        
        # Create user account
        user_id = db_manager.create_user(email, password, face_encoding)
        if user_id:
            # Save face encoding to both database and file for redundancy
            face_service.save_face_encoding(user_id, face_encoding)
            
            # Generate Z-secure key from facial biometrics
            zsecure_key = zsecure.generate_key_from_biometrics(face_encoding, email)
            db_manager.store_zsecure_key(user_id, zsecure_key)
            
            flash('Account created successfully! Please log in.', 'success')
            return jsonify({'success': True, 'redirect': url_for('login')})
        else:
            return jsonify({'success': False, 'message': 'Failed to create account'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with facial authentication"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        # Verify credentials
        user = db_manager.verify_user_credentials(email, password)
        if not user:
            flash('Invalid email or password', 'error')
            return render_template('login.html')
        
        return render_template('face_auth.html', user_id=user['id'], email=email)
    
    return render_template('login.html')

@app.route('/authenticate_face', methods=['POST'])
def authenticate_face():
    """Facial authentication for login"""
    try:
        user_id = request.form.get('user_id')
        face_data = request.form.get('face_data')
        
        print(f"Authentication attempt for user {user_id}")
        
        if not face_data:
            return jsonify({'success': False, 'message': 'No facial data received'})
        
        if not user_id:
            return jsonify({'success': False, 'message': 'No user ID provided'})
        
        print(f"Face data length: {len(face_data)} characters")
        
        # Verify facial authentication
        verification_result = face_service.verify_face(user_id, face_data)
        print(f"Face verification result: {verification_result}")
        
        if verification_result:
            # Create session
            session_id = session_manager.create_session(user_id)
            session['user_id'] = user_id
            session['session_id'] = session_id
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=15)
            
            print(f"Authentication successful for user {user_id}")
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        else:
            print(f"Authentication failed for user {user_id}")
            return jsonify({'success': False, 'message': 'Facial authentication failed. Please ensure good lighting and try again.'})
            
    except Exception as e:
        print(f"Authentication error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Authentication failed: {str(e)}'})

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard for authenticated users"""
    user = db_manager.get_user(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/process_image', methods=['POST'])
@login_required
def process_image():
    """Process uploaded image - encrypt or decrypt based on detection"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image uploaded'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No image selected'})
        
        if not image_processor.allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type'})
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Get user's Z-secure key
        zsecure_key = db_manager.get_zsecure_key(session['user_id'])
        
        # Detect if image is encrypted or normal
        is_encrypted = image_processor.detect_encryption(filepath)
        
        if is_encrypted:
            # Decrypt the image
            result_path = zsecure.decrypt_image(filepath, zsecure_key)
            operation = 'decryption'
        else:
            # Encrypt the image
            result_path = zsecure.encrypt_image(filepath, zsecure_key)
            operation = 'encryption'
        
        # Log the operation
        db_manager.log_operation(session['user_id'], operation, filename)
        
        # Clean up original file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'operation': operation,
            'download_url': url_for('download_file', filename=os.path.basename(result_path))
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Processing failed: {str(e)}'})

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Download processed file"""
    try:
        filepath = os.path.join('processed', filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f'Download failed: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/manage_face')
@login_required
def manage_face():
    """Face management page"""
    user = db_manager.get_user(session['user_id'])
    face_data = db_manager.get_face_data(session['user_id'])
    return render_template('manage_face.html', user=user, face_data=face_data)

@app.route('/update_face', methods=['POST'])
@login_required
def update_face():
    """Update facial data"""
    try:
        face_data = request.form.get('face_data')
        
        if not face_data:
            return jsonify({'success': False, 'message': 'No facial data received'})
        
        # Process new facial data
        face_encoding = face_service.process_face_data(face_data)
        if face_encoding is None:
            return jsonify({'success': False, 'message': 'Could not detect face. Please try again.'})
        
        # Update face data and regenerate Z-secure key
        user = db_manager.get_user(session['user_id'])
        new_zsecure_key = zsecure.generate_key_from_biometrics(face_encoding, user['email'])
        
        db_manager.update_face_data(session['user_id'], face_encoding)
        db_manager.update_zsecure_key(session['user_id'], new_zsecure_key)
        
        return jsonify({'success': True, 'message': 'Facial data updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Update failed: {str(e)}'})

@app.route('/history')
@login_required
def history():
    """View operation history"""
    operations = db_manager.get_user_operations(session['user_id'])
    
    # Handle AJAX requests
    if request.args.get('ajax') == '1':
        limit = int(request.args.get('limit', 10))
        limited_operations = operations[:limit] if operations else []
        
        # Convert operations to JSON-serializable format
        operations_data = []
        for op in limited_operations:
            operations_data.append({
                'id': op.get('id', ''),
                'operation_type': op.get('operation_type', ''),
                'filename': op.get('filename', ''),
                'status': 'success' if op.get('success') else 'failed',
                'created_at': op.get('timestamp', ''),  # Use timestamp from DB
                'file_size': op.get('file_size', 0)
            })
        
        return jsonify({
            'success': True,
            'operations': operations_data,
            'total': len(operations) if operations else 0
        })
    
    return render_template('history.html', operations=operations)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account permanently"""
    try:
        # Get current user info for validation
        current_user = db_manager.get_user(session['user_id'])
        if not current_user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Verify password for security
        password = request.form.get('password')
        if not password:
            return jsonify({'success': False, 'message': 'Password verification required'})
        
        # Re-verify user credentials
        user_verification = db_manager.verify_user_credentials(current_user['email'], password)
        if not user_verification:
            return jsonify({'success': False, 'message': 'Invalid password. Account deletion cancelled.'})
        
        user_id = session['user_id']
        
        # Clean up user files first
        db_manager.cleanup_user_files(user_id)
        
        # Invalidate all user sessions
        if 'session_id' in session:
            session_manager.invalidate_session(session['session_id'])
        
        # Delete user account and all associated data
        deletion_success = db_manager.delete_user_account(user_id)
        
        if deletion_success:
            # Clear session
            session.clear()
            
            return jsonify({
                'success': True, 
                'message': 'Account successfully deleted. You will be redirected to the home page.',
                'redirect': url_for('index')
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to delete account. Please try again.'})
            
    except Exception as e:
        print(f"Error deleting account: {e}")
        return jsonify({'success': False, 'message': f'Account deletion failed: {str(e)}'})

@app.route('/logout')
def logout():
    """User logout"""
    if 'session_id' in session:
        session_manager.invalidate_session(session['session_id'])
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.before_request
def check_session_timeout():
    """Check session timeout before each request"""
    if 'user_id' in session:
        if not session_manager.is_session_valid(session.get('session_id')):
            session.clear()
            if request.endpoint not in ['index', 'login', 'register']:
                flash('Session expired. Please log in again.', 'warning')
                return redirect(url_for('login'))

if __name__ == '__main__':
    # Initialize database
    db_manager.init_database()
    
    # Create processed directory
    os.makedirs('processed', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
