#!/usr/bin/env python3
"""
EncryptPro v2 - Enterprise Image Security Platform
Production deployment script
"""

import os
import sys
from app import app
from src.database_manager import DatabaseManager

def setup_production():
    """Setup production environment"""
    print("Setting up EncryptPro v2 for production...")
    
    # Create necessary directories
    directories = ['uploads', 'processed', 'face_data', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.init_database()
    print("✓ Database initialized")
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    print("✓ Environment set to production")
    
    print("\nEncryptPro v2 is ready for production!")
    print("Make sure to:")
    print("1. Set SECRET_KEY environment variable")
    print("2. Configure SSL certificate")
    print("3. Set up reverse proxy (nginx/apache)")
    print("4. Configure firewall rules")
    print("5. Set up monitoring and logging")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        setup_production()
    else:
        # Production server
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
