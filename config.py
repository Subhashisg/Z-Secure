# Z-Secure Configuration
import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zsecure-v3-enterprise-security-key-2025'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'zsecure.db'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    PROCESSED_FOLDER = os.environ.get('PROCESSED_FOLDER') or 'processed'
    FACE_DATA_FOLDER = os.environ.get('FACE_DATA_FOLDER') or 'face_data'
    
    # File upload settings
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILE_SIZE', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    
    # Session settings
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 900))  # 15 minutes
    PERMANENT_SESSION_LIFETIME = SESSION_TIMEOUT
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security settings
    FACE_RECOGNITION_TOLERANCE = float(os.environ.get('FACE_TOLERANCE', 0.4))
    MAX_FAILED_ATTEMPTS = int(os.environ.get('MAX_FAILED_ATTEMPTS', 5))
    LOCKOUT_DURATION = int(os.environ.get('LOCKOUT_DURATION', 1800))  # 30 minutes
    
    # Encryption settings
    ENCRYPTION_KEY_LENGTH = 32  # 256 bits
    ENCRYPTION_IV_LENGTH = 16   # 128 bits
    CHAOS_ITERATIONS = int(os.environ.get('CHAOS_ITERATIONS', 1000))
    PBKDF2_ITERATIONS = int(os.environ.get('PBKDF2_ITERATIONS', 100000))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_PATH = ':memory:'  # In-memory database for testing
    SESSION_TIMEOUT = 60  # Shorter timeout for testing

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
