#!/usr/bin/env python3
"""
WSGI Configuration for Z-Secure
Z-Secure - Enterprise Security Platform

This module contains the WSGI configuration for deploying Z-Secure
in production environments using servers like Gunicorn, uWSGI, or Apache mod_wsgi.
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup the production environment"""
    print("Setting up Z-Secure for production...")
    
    # Add the application directory to Python path
    app_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, app_dir)
    
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    os.makedirs('face_data', exist_ok=True)

# Setup environment
setup_environment()

# Import the Flask application
from app import app

# WSGI application entry point
application = app

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
