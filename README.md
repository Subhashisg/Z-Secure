# EncryptPro v2 - Enterprise Image Security Platform

![Z-Secure](https://img.shields.io/badge/EncryptPro-v2.0-blue.svg)
![Security](https://img.shields.io/badge/Security-Enterprise%20Grade-green.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-red.svg)

## Overview

EncryptPro v2 is an enterprise-grade web application for image encryption and decryption using advanced Z-Secure algorithms with facial biometric authentication. The platform combines chaos theory-based encryption with biometric key derivation for unparalleled security.

## Features

### 🔐 **Advanced Security**
- **Z-Secure Encryption Algorithm**: Chaos-based encryption with biometric key derivation
- **Facial Authentication**: Advanced AI-powered face recognition for user authentication
- **256-bit AES Encryption**: Industry-standard encryption with custom enhancements
- **Biometric Key Derivation**: Encryption keys derived from unique facial biometrics
- **Anti-Spoofing Protection**: Real-time liveness detection during authentication

### 🎯 **Core Functionality**
- **Smart Image Detection**: Automatically detects encrypted vs normal images
- **One-Click Processing**: Seamless encryption/decryption with single upload
- **Instant Downloads**: Direct download of processed images
- **Batch Processing**: Handle multiple images efficiently
- **Format Support**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP

### 🛡️ **Enterprise Features**
- **Session Management**: Short timeout with tab closure detection (15 minutes)
- **Activity Logging**: Complete audit trail of all operations
- **Face Management**: Update biometric data with key regeneration
- **Security Events**: Real-time threat detection and monitoring
- **Export/Import**: Backup and restore encryption keys

### 🎨 **User Experience**
- **Responsive Design**: Mobile-friendly interface
- **Real-time Feedback**: Live session timer and processing status
- **Intuitive Dashboard**: Clean, modern interface
- **Progressive Web App**: Installable on mobile devices

## Technology Stack

- **Backend**: Flask 2.3+ (Python)
- **Database**: SQLite with enterprise schema
- **Encryption**: Cryptography library with custom algorithms
- **Face Recognition**: face_recognition + OpenCV
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Security**: PBKDF2, HMAC, session management

## Installation

### Prerequisites
- Python 3.8 or higher
- Web camera for facial authentication
- Modern web browser with camera support

### Quick Start

1. **Clone or download the project**
   ```bash
   cd EncryptPro_v2
   ```

2. **Run the startup script (Windows)**
   ```bash
   start.bat
   ```

3. **Manual installation (All platforms)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the application
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Usage Guide

### 1. Registration
1. Navigate to the registration page
2. Enter email and password
3. Capture facial biometric data using your camera
4. Complete account creation

### 2. Login
1. Enter email and password
2. Complete facial authentication
3. Access your secure dashboard

### 3. Image Processing
1. Upload any image file
2. System automatically detects if image is encrypted or normal
3. Processing occurs automatically with your biometric key
4. Download the result instantly

### 4. Face Management
1. Navigate to Face Management
2. Update your facial biometric data
3. System regenerates encryption keys automatically
4. Previous images remain accessible

## Security Architecture

### Z-Secure Algorithm
```
User Face Data + Email → Chaos Algorithm → PBKDF2 → AES-256 Key
```

### Key Features:
- **Lorenz Attractor**: Chaos theory implementation for key enhancement
- **Biometric Binding**: Keys tied to individual facial characteristics
- **Salt Generation**: Unique salt per user for key derivation
- **Zero Knowledge**: Server never stores actual encryption keys

### Session Security
- 15-minute automatic timeout
- Tab closure detection
- Failed attempt lockout (5 attempts = 30-minute lockout)
- Session token rotation
- IP address tracking

## API Documentation

### Core Endpoints

```http
POST /register          # User registration
POST /capture_face      # Facial biometric capture
POST /login             # User authentication
POST /authenticate_face # Facial authentication
POST /process_image     # Image encryption/decryption
POST /update_face       # Update facial data
GET  /history          # Operation history
GET  /manage_face      # Face management interface
```

### Response Format
```json
{
    "success": true|false,
    "message": "status message",
    "data": {...},
    "redirect": "url"
}
```

## Database Schema

### Users Table
- User credentials and account information
- Failed login attempt tracking
- Account lockout management

### Face Data Table
- Encrypted facial biometric encodings
- Creation and update timestamps
- User relationship mapping

### Sessions Table
- Active session management
- Timeout and expiration tracking
- Security event correlation

### Operations Log Table
- Complete audit trail
- File processing history
- Success/failure tracking

### Security Events Table
- Authentication attempts
- System security events
- Threat detection logs

## Configuration

### Environment Variables
```bash
FLASK_ENV=production          # Development/Production mode
SESSION_TIMEOUT=900           # Session timeout in seconds
MAX_FILE_SIZE=16777216       # Maximum file size (16MB)
DATABASE_PATH=encryptpro.db  # Database file location
```

### Security Settings
- **Session Timeout**: 15 minutes (configurable)
- **File Size Limit**: 16MB (configurable)
- **Failed Attempts**: 5 attempts before lockout
- **Lockout Duration**: 30 minutes
- **Encryption**: 256-bit AES with CBC mode

## Troubleshooting

### Common Issues

1. **Camera Access Denied**
   - Ensure browser permissions are granted
   - Check system camera settings
   - Try refreshing the page

2. **Face Recognition Fails**
   - Ensure good lighting conditions
   - Remove glasses if worn during registration
   - Keep face centered and steady

3. **Session Timeout**
   - Activity resets the timer
   - Close unnecessary browser tabs
   - Ensure stable internet connection

4. **Installation Issues**
   - Verify Python 3.8+ is installed
   - Check camera hardware compatibility
   - Ensure all dependencies install correctly

### Error Codes

- `AUTH_001`: Invalid credentials
- `AUTH_002`: Facial authentication failed
- `AUTH_003`: Account locked due to failed attempts
- `PROC_001`: Image processing failed
- `PROC_002`: Unsupported file format
- `PROC_003`: File size too large

## Security Considerations

### Data Protection
- All facial data encrypted at rest
- Biometric templates cannot reconstruct original images
- Keys derived locally, never transmitted
- GDPR and CCPA compliant design

### Best Practices
- Use strong passwords
- Keep biometric data updated
- Regular security audits
- Monitor activity logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit pull request

## License

This project is licensed under the Enterprise Security License - see the LICENSE file for details.

## Support

For enterprise support and licensing:
- Email: support@encryptpro.com
- Documentation: https://docs.encryptpro.com
- Issue Tracker: GitHub Issues

## Changelog

### v2.0.0 (Current)
- Z-Secure encryption algorithm implementation
- Facial biometric authentication
- Enterprise session management
- Complete audit logging
- Responsive web interface

### v1.0.0
- Basic image encryption
- Password-based authentication
- Simple file management

---

**⚠️ Security Notice**: This application handles sensitive biometric data. Ensure compliance with local privacy laws and implement additional security measures for production deployment.

**🔒 Enterprise Ready**: Contact us for enterprise licensing, custom deployment, and dedicated support options.
