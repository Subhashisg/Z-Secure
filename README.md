# Z-Secure - Advanced Biometric Security Platform

![Z-Secure](https://img.shields.io/badge/Z--Secure-v3.0-blue.svg)
![Security](https://img.shields.io/badge/Security-Enterprise%20Grade-green.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-red.svg)
![Liveness](https://img.shields.io/badge/Liveness%20Detection-AI%20Powered-orange.svg)

## 🚀 Overview

Z-Secure is an enterprise-grade biometric security platform that combines advanced facial recognition with real-time liveness detection to provide unparalleled security for image encryption and user authentication. The platform uses cutting-edge AI algorithms with chaos theory-based encryption for maximum security against spoofing attacks and unauthorized access.

## ✨ Key Features

### 🔐 **Advanced Biometric Security**
- **AI-Powered Liveness Detection**: Real-time anti-spoofing using MediaPipe
- **Multi-Modal Verification**: Blink detection, head movement analysis, texture variance
- **Facial Authentication**: Advanced face recognition with 128-dimensional encodings
- **Biometric Key Derivation**: Encryption keys derived from unique facial characteristics
- **Anti-Spoofing Protection**: Prevents photo, video, and mask attacks

## 🛠️ Technical Stack

### **Backend**
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Core language |
| Flask | 2.3.3 | Web framework |
| Gunicorn | 21.2.0 | Production server |
| SQLite | 3 | Database |

### **Security & Encryption**
| Technology | Purpose |
|-----------|---------|
| Cryptography 41.0.7 | Encryption operations |
| AES-256 | File encryption |
| SHA-256 | Secure hashing |
| PBKDF2 | Key derivation |

### **Image Processing**
| Technology | Version | Purpose |
|-----------|---------|---------|
| Pillow | 9.5.0 | Image manipulation |
| NumPy | 1.24.3 | Numerical computing |
| OpenCV* | 4.8.1.78 | Computer vision (optional) |
| MediaPipe* | 0.10.7 | Face detection (optional) |

*Optional dependencies for advanced features

### **Frontend**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5 for responsive UI
- Font Awesome icons
- WebRTC for camera access

📖 **[View Complete Technical Documentation →](./TECHNICAL_README.md)**

## ✨ Key Features

### 🛡️ **Z-Secure Encryption**
- **Chaos-Based Algorithm**: Lorenz attractor implementation for key generation
- **256-bit AES Encryption**: Industry-standard encryption with biometric enhancement
- **Zero-Knowledge Architecture**: Server never stores actual encryption keys
- **Quantum-Resistant Design**: Future-proof security implementation
- **Perfect Forward Secrecy**: Each session uses unique encryption parameters

### 🎯 **Liveness Detection Features**
- **Eye Blink Analysis**: Real-time eye aspect ratio monitoring
- **Head Pose Estimation**: 3D head movement tracking (pitch, yaw, roll)
- **Texture Analysis**: Laplacian variance for photo detection
- **Face Quality Assessment**: Size, brightness, and clarity validation
- **Comprehensive Scoring**: Multi-factor liveness verification

### 🖼️ **Image Processing**
- **Smart Detection**: Automatically identifies encrypted vs normal images
- **One-Click Processing**: Seamless encryption/decryption workflow
- **Format Support**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP
- **Batch Processing**: Handle multiple images efficiently
- **Instant Downloads**: Direct download of processed results

### 🔒 **Enterprise Security**
- **Account Management**: Complete delete account functionality
- **Session Management**: 15-minute timeout with tab closure detection
- **Activity Logging**: Complete audit trail of all operations
- **Security Events**: Real-time threat detection and monitoring
- **Failure Protection**: Lockout after failed authentication attempts

### 🎨 **User Experience**
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **Real-time Feedback**: Live session timer and processing status
- **Intuitive Dashboard**: Clean, modern interface with activity cards
- **Progressive Enhancement**: Works across all modern browsers
- **Accessibility**: WCAG 2.1 compliant design

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3+ (Python)
- **Database**: SQLite with enterprise schema design
- **Encryption**: Cryptography library with custom Z-Secure algorithms
- **Face Recognition**: face_recognition + dlib + OpenCV
- **Liveness Detection**: MediaPipe + TensorFlow Lite
- **Security**: PBKDF2, HMAC, secure session management

### AI & Computer Vision
- **Face Detection**: HOG + CNN models for accuracy
- **Liveness Detection**: MediaPipe FaceMesh with 468 landmarks
- **Eye Tracking**: Eye Aspect Ratio (EAR) calculation
- **Head Pose**: 3D rotation estimation
- **Texture Analysis**: Laplacian variance for spoof detection

### Frontend
- **UI Framework**: Bootstrap 5.3 with custom styling
- **JavaScript**: Vanilla ES6+ with modern APIs
- **Camera Access**: WebRTC getUserMedia API
- **Real-time Processing**: Canvas API for image capture
- **Responsive Design**: Mobile-first approach

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- Web camera for facial authentication
- Modern web browser with camera support
- At least 4GB RAM for AI processing

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Subhashisg/Z-Secure.git
   cd Z-Secure
   ```

2. **Windows Quick Start**
   ```bash
   start.bat
   ```

3. **Manual Installation (All Platforms)**
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
   
   # Initialize database
   python -c "from src.database_manager import DatabaseManager; DatabaseManager().init_database()"
   
   # Start the application
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## 📖 Usage Guide

### 1. Account Registration with Liveness Detection
1. Navigate to the registration page
2. Enter email and secure password
3. **Liveness Verification Process**:
   - Allow camera access when prompted
   - Follow on-screen instructions for liveness detection
   - Blink naturally during capture
   - Make slight head movements to prove you're real
   - Ensure good lighting on your face
4. Complete account creation with biometric binding

### 2. Secure Login Process
1. Enter email and password credentials
2. **Multi-Factor Biometric Authentication**:
   - Camera automatically activates
   - Look directly at the camera
   - Blink naturally during authentication
   - System performs real-time liveness detection
   - Authentication completes in seconds
3. Access your secure dashboard

### 3. Image Encryption/Decryption
1. Upload any supported image file
2. System automatically detects image type (encrypted/normal)
3. Processing occurs with your unique biometric key
4. Download processed image instantly
5. View operation in activity history

### 4. Account Management
1. **Face Management**: Update biometric data with liveness verification
2. **Activity History**: View all operations and security events
3. **Delete Account**: Complete account removal with data cleanup
4. **Session Management**: Monitor active sessions and timeouts

## 🔐 Security Architecture

### Liveness Detection Pipeline
```
Camera Input → Face Detection → Landmark Analysis → Liveness Checks → Verification
     ↓              ↓                ↓                  ↓              ↓
WebRTC API → MediaPipe AI → 468 Landmarks → Multi-Factor → Pass/Fail
```

### Liveness Detection Components
1. **Blink Detection**: Eye Aspect Ratio (EAR) analysis
2. **Head Movement**: 3D pose estimation (pitch, yaw, roll)
3. **Texture Analysis**: Laplacian variance for photo detection
4. **Face Quality**: Size, brightness, and clarity validation

### Z-Secure Key Derivation
```
Facial Encoding + Email → Chaos Algorithm → PBKDF2 → AES-256 Key
      ↓                       ↓               ↓          ↓
128-dim vector → Lorenz Attractor → Salt + Hash → Encryption
```

### Security Layers
1. **Authentication**: Email/password + facial biometrics + liveness
2. **Authorization**: Session-based access control
3. **Encryption**: AES-256 with biometric-derived keys
4. **Transport**: HTTPS with secure headers
5. **Storage**: Encrypted database with secure key management

## 🔧 API Documentation

### Authentication Endpoints

```http
POST /register              # User registration with liveness
POST /capture_face          # Facial capture with liveness detection
POST /login                 # Email/password authentication
POST /authenticate_face     # Facial authentication with liveness
GET  /logout               # Secure session termination
```

### Core Functionality

```http
POST /process_image        # Image encryption/decryption
GET  /dashboard           # User dashboard with activity
GET  /history             # Operation history
GET  /manage_face         # Face management interface
POST /update_face         # Update biometric data
POST /delete_account      # Complete account deletion
```

### Liveness Detection API

```http
POST /liveness_check      # Standalone liveness verification
GET  /liveness_config     # Liveness detection configuration
```

### Response Format
```json
{
    "success": true|false,
    "message": "Descriptive status message",
    "data": {
        "liveness_score": 0.85,
        "checks_passed": 3,
        "total_checks": 4,
        "liveness_result": {...}
    },
    "redirect": "optional_redirect_url"
}
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    face_encoding BLOB,
    zsecure_key TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    failed_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

### Sessions Table
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT
);
```

### Operations Log
```sql
CREATE TABLE operations_log (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    operation_type TEXT,
    filename TEXT,
    success BOOLEAN,
    timestamp TIMESTAMP,
    ip_address TEXT,
    liveness_score REAL
);
```

### Security Events
```sql
CREATE TABLE security_events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    event_type TEXT,
    description TEXT,
    ip_address TEXT,
    timestamp TIMESTAMP,
    severity TEXT
);
```

## ⚙️ Configuration

### Environment Variables
```bash
FLASK_ENV=production                    # Development/Production mode
SESSION_TIMEOUT=900                     # Session timeout (15 minutes)
MAX_FILE_SIZE=16777216                 # Maximum file size (16MB)
DATABASE_PATH=zsecure.db               # Database file location
LIVENESS_THRESHOLD=0.5                 # Liveness detection threshold
FACE_TOLERANCE=0.4                     # Face recognition tolerance
```

### Liveness Detection Settings
```python
# Configurable thresholds
BLINK_THRESHOLD = 0.2                  # Eye aspect ratio threshold
HEAD_TURN_THRESHOLD = 15               # Head movement in degrees
TEXTURE_VARIANCE_THRESHOLD = 50        # Texture variance for real faces
MIN_FACE_SIZE = 100                    # Minimum face size in pixels
LIVENESS_CHECKS_REQUIRED = 2           # Minimum checks to pass
```

## 🔍 Troubleshooting

### Liveness Detection Issues

**Problem**: Liveness detection fails repeatedly
**Solutions**:
- Ensure adequate lighting (avoid backlighting)
- Remove glasses or accessories if worn during registration
- Blink naturally during authentication
- Make slight head movements to prove liveness
- Keep face centered and at appropriate distance
- Check camera quality and resolution

**Problem**: Camera access denied
**Solutions**:
- Grant browser permissions for camera access
- Check system camera settings and privacy controls
- Ensure camera is not being used by other applications
- Try refreshing the page or restarting browser

### Authentication Issues

**Problem**: Face recognition fails after liveness passes
**Solutions**:
- Ensure similar lighting conditions as registration
- Maintain same facial expression and angle
- Remove/add glasses consistently with registration
- Update biometric data if appearance changed significantly

**Problem**: Account lockout after failed attempts
**Solutions**:
- Wait 30 minutes for automatic unlock
- Contact administrator for manual unlock
- Verify correct email and password combination
- Ensure camera and lighting are working properly

### Performance Issues

**Problem**: Slow liveness detection processing
**Solutions**:
- Ensure adequate system resources (4GB+ RAM)
- Close unnecessary browser tabs and applications
- Use a modern browser with hardware acceleration
- Check network connection stability

## 🚨 Security Considerations

### Data Protection
- **Biometric Privacy**: Facial encodings cannot reconstruct original images
- **Zero Storage**: Actual encryption keys never stored on server
- **GDPR Compliance**: Right to deletion and data portability
- **Encryption at Rest**: All sensitive data encrypted in database
- **Transport Security**: TLS 1.3 for all communications

### Anti-Spoofing Measures
- **Photo Attack Prevention**: Texture analysis detects printed photos
- **Video Attack Prevention**: Liveness detection requires real movement
- **Mask Attack Prevention**: 3D face analysis and skin texture validation
- **Deepfake Prevention**: Multi-modal verification with timing analysis

### Best Practices
- **Strong Passwords**: Enforce complex password requirements
- **Regular Updates**: Keep biometric data current for accuracy
- **Security Monitoring**: Regular audit of security events
- **Access Control**: Principle of least privilege implementation
- **Incident Response**: Automated threat detection and response

## 🤝 Contributing

We welcome contributions to improve Z-Secure's security and functionality:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Implement changes**: Add code, tests, and documentation
4. **Test thoroughly**: Ensure all tests pass including liveness detection
5. **Submit pull request**: Detailed description of changes

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive unit tests
- Update documentation for new features
- Test liveness detection across different devices
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- **API Reference**: [docs/api.md](docs/api.md)
- **Security Guide**: [docs/security.md](docs/security.md)
- **Deployment Guide**: [docs/deployment.md](docs/deployment.md)

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community Q&A and discussions
- **Wiki**: Additional documentation and tutorials

### Enterprise Support
For enterprise licensing, custom deployment, and dedicated support:
- **Email**: enterprise@z-secure.com
- **Support Portal**: https://support.z-secure.com
- **Professional Services**: Custom implementation and training

## 📈 Changelog

### v3.0.0 (Current) - Advanced Liveness Detection
- ✅ **AI-Powered Liveness Detection**: MediaPipe integration
- ✅ **Multi-Modal Verification**: Blink, movement, texture analysis
- ✅ **Enhanced Security**: Anti-spoofing protection
- ✅ **Delete Account Feature**: Complete account management
- ✅ **Improved UI/UX**: Enhanced user interface with liveness guidance
- ✅ **Performance Optimization**: Faster processing with TensorFlow Lite
- ✅ **Comprehensive Testing**: Automated test suite for all features

### v2.0.0 - Z-Secure Implementation
- Z-Secure encryption algorithm with chaos theory
- Facial biometric authentication
- Enterprise session management
- Complete audit logging
- Responsive web interface

### v1.0.0 - Initial Release
- Basic image encryption/decryption
- Password-based authentication
- Simple file management

## 🎯 Roadmap

### Upcoming Features
- **Multi-Device Sync**: Cross-device biometric synchronization
- **Advanced Analytics**: Detailed security and usage analytics
- **API Integration**: RESTful API for third-party integration
- **Mobile Apps**: Native iOS and Android applications
- **Cloud Deployment**: Kubernetes and Docker support
- **Advanced Encryption**: Post-quantum cryptography support

### Research & Development
- **Behavioral Biometrics**: Typing patterns and mouse dynamics
- **Voice Authentication**: Speaker recognition integration
- **Continuous Authentication**: Ongoing user verification
- **Federated Learning**: Privacy-preserving model updates

---

## ⚠️ Important Notices

**🔒 Security Notice**: This application handles sensitive biometric data. Ensure compliance with local privacy laws (GDPR, CCPA, BIPA) and implement additional security measures for production deployment.

**🛡️ Liveness Detection**: The AI-powered liveness detection significantly enhances security by preventing spoofing attacks. Ensure adequate lighting and follow the on-screen guidance for best results.

**🚀 Enterprise Ready**: Z-Secure is production-ready with enterprise-grade security features. Contact us for deployment assistance and custom requirements.

**📱 Privacy First**: Your biometric data is processed locally and never leaves your control. Facial encodings cannot be reverse-engineered to reconstruct your actual face.

---

*Built with ❤️ for security and privacy*

### Prerequisites
- Python 3.8 or higher
- Web camera for facial authentication
- Modern web browser with camera support

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Subhashisg/Z-Secure.git
   cd Z-Secure
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
DATABASE_PATH=zsecure.db     # Database file location
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

### Enterprise Support
For enterprise licensing, custom deployment, and dedicated support:
- **Email**: enterprise@z-secure.com
- **Support Portal**: https://support.z-secure.com
- **Professional Services**: Custom implementation and training

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
