# Liveness Detection Implementation Guide

## Overview

The Z-Secure platform implements state-of-the-art liveness detection to prevent spoofing attacks and ensure that only real, living users can authenticate. This document provides detailed information about the liveness detection system.

## Architecture

### Core Components

1. **LivenessDetector Class** (`src/liveness_detector.py`)
   - Main liveness detection engine
   - MediaPipe integration for face analysis
   - Multi-modal verification system

2. **Face Recognition Integration** (`src/face_recognition_service.py`)
   - Seamless integration with existing face recognition
   - Liveness-enabled authentication pipeline
   - Backward compatibility support

3. **Frontend Integration** (Templates)
   - Real-time camera feed processing
   - User guidance and feedback
   - Progressive enhancement

## Liveness Detection Methods

### 1. Blink Detection
- **Technology**: Eye Aspect Ratio (EAR) calculation
- **Landmarks**: 16 eye landmarks per eye (32 total)
- **Threshold**: 0.2 (configurable)
- **Purpose**: Detects natural eye blinking patterns

```python
def calculate_eye_aspect_ratio(self, landmarks, eye_idxs):
    # Extract eye landmarks
    eye_points = [landmarks[idx] for idx in eye_idxs]
    
    # Calculate vertical and horizontal distances
    v1 = distance(eye_points[1], eye_points[5])
    v2 = distance(eye_points[2], eye_points[4])
    h = distance(eye_points[0], eye_points[3])
    
    # Eye Aspect Ratio
    ear = (v1 + v2) / (2.0 * h)
    return ear
```

### 2. Head Movement Detection
- **Technology**: 3D pose estimation
- **Parameters**: Pitch, Yaw, Roll angles
- **Threshold**: 15 degrees (configurable)
- **Purpose**: Detects natural head movements

```python
def detect_head_movement(self, image):
    # Extract key facial landmarks
    nose_tip = landmarks[1]
    chin = landmarks[18]
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    
    # Calculate head pose angles
    yaw = calculate_yaw(nose_tip, eye_center)
    pitch = calculate_pitch(nose_tip, eye_center)
    roll = calculate_roll(left_eye, right_eye)
    
    return {
        'head_pose': {'pitch': pitch, 'yaw': yaw, 'roll': roll},
        'movement_detected': abs(yaw) > threshold or abs(pitch) > threshold
    }
```

### 3. Texture Analysis
- **Technology**: Laplacian variance calculation
- **Threshold**: 50 (configurable)
- **Purpose**: Detects printed photos and screens

```python
def analyze_texture_variance(self, image):
    # Convert to grayscale and extract face region
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_region = extract_face_region(gray)
    
    # Calculate Laplacian variance
    laplacian = cv2.Laplacian(face_region, cv2.CV_64F)
    variance = laplacian.var()
    
    return {
        'variance': variance,
        'is_real': variance > self.texture_variance_threshold
    }
```

### 4. Face Quality Assessment
- **Parameters**: Size, brightness, area ratio
- **Min Face Size**: 100 pixels (configurable)
- **Brightness Range**: 50-200 (0-255 scale)
- **Purpose**: Ensures adequate image quality

## Scoring System

### Comprehensive Liveness Score
The system combines all detection methods into a single score:

```python
def comprehensive_liveness_check(self, image):
    # Run all checks
    blink_result = self.detect_blink(image)
    movement_result = self.detect_head_movement(image)
    texture_result = self.analyze_texture_variance(image)
    quality_result = self.check_face_quality(image)
    
    # Calculate weighted score
    liveness_score = 0.0
    checks_passed = 0
    
    # Each check contributes 25% to the total score
    if blink_result['blink_detected'] or blink_result['avg_ear'] > 0.15:
        liveness_score += 0.25
        checks_passed += 1
    
    if movement_result['movement_detected']:
        liveness_score += 0.25
        checks_passed += 1
    
    if texture_result['is_real']:
        liveness_score += 0.25
        checks_passed += 1
    
    if quality_result['quality_sufficient'] and quality_result['brightness_ok']:
        liveness_score += 0.25
        checks_passed += 1
    
    # Pass criteria: at least 2/4 checks or score >= 0.5
    liveness_passed = checks_passed >= 2 or liveness_score >= 0.5
    
    return {
        'liveness_passed': liveness_passed,
        'liveness_score': liveness_score,
        'checks_passed': checks_passed,
        'total_checks': 4
    }
```

## Integration Points

### 1. Registration Process
```python
# During account registration
processing_result = face_service.process_face_data_with_liveness(
    face_data_b64, 
    require_liveness=True
)

if processing_result['success']:
    # Create account with verified biometric data
    user_id = create_user(email, password, processing_result['encoding'])
else:
    # Handle liveness detection failure
    return error_response(processing_result['error'])
```

### 2. Authentication Process
```python
# During login authentication
verification_result = face_service.verify_face_with_liveness(
    user_id, 
    face_data_b64, 
    require_liveness=True
)

if verification_result['success']:
    # Create secure session
    create_session(user_id)
    return success_response()
else:
    # Handle authentication failure
    log_security_event(user_id, 'LIVENESS_FAILED')
    return error_response(verification_result['error'])
```

## Configuration

### Adjustable Parameters

```python
# In LivenessDetector.__init__()
class LivenessDetector:
    def __init__(self):
        # Blink detection
        self.blink_threshold = 0.2
        
        # Head movement detection
        self.head_turn_threshold = 15  # degrees
        
        # Texture analysis
        self.texture_variance_threshold = 50
        
        # Face quality
        self.min_face_size = 100  # pixels
        
        # MediaPipe configuration
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
```

### Environment-Specific Tuning

```python
# Development environment (more lenient)
LIVENESS_THRESHOLD = 0.3
BLINK_THRESHOLD = 0.25
HEAD_TURN_THRESHOLD = 20

# Production environment (strict)
LIVENESS_THRESHOLD = 0.5
BLINK_THRESHOLD = 0.2
HEAD_TURN_THRESHOLD = 15

# High-security environment (very strict)
LIVENESS_THRESHOLD = 0.75
BLINK_THRESHOLD = 0.15
HEAD_TURN_THRESHOLD = 10
```

## Security Considerations

### Attack Vectors Prevented

1. **Photo Attacks**
   - Printed photographs
   - Digital displays
   - Static images

2. **Video Attacks**
   - Pre-recorded videos
   - Deepfake videos
   - Video displays

3. **Mask Attacks**
   - Physical masks
   - 3D printed faces
   - Silicone prosthetics

### Limitations

1. **Environmental Factors**
   - Poor lighting conditions
   - Camera quality limitations
   - Network latency issues

2. **User Factors**
   - Unusual facial features
   - Medical conditions affecting movement
   - Accessibility considerations

3. **Technical Factors**
   - Browser compatibility
   - Device performance
   - MediaPipe model limitations

## Performance Optimization

### Efficient Processing
- TensorFlow Lite for mobile optimization
- Landmark caching for repeated operations
- Parallel processing of liveness checks
- Optimized image preprocessing

### Memory Management
- Proper cleanup of MediaPipe resources
- Image buffer management
- Session-based processing limits

## Testing and Validation

### Unit Tests
```python
def test_liveness_detection():
    detector = LivenessDetector()
    
    # Test with synthetic image
    result = detector.comprehensive_liveness_check(test_image)
    assert 'liveness_passed' in result
    assert 'liveness_score' in result
    
    # Test individual components
    blink_result = detector.detect_blink(test_image)
    assert 'blink_detected' in blink_result
```

### Integration Tests
```python
def test_face_recognition_with_liveness():
    face_service = FaceRecognitionService()
    
    # Test processing with liveness
    result = face_service.process_face_data_with_liveness(
        face_data_b64, 
        require_liveness=True
    )
    
    assert 'success' in result
    assert 'liveness_result' in result
```

## Troubleshooting

### Common Issues

1. **MediaPipe Installation**
   ```bash
   pip install mediapipe==0.10.7
   # Ensure NumPy compatibility
   pip install "numpy<2"
   ```

2. **Camera Access**
   - Browser permissions
   - HTTPS requirement for camera access
   - Device camera availability

3. **Performance Issues**
   - System resources (4GB+ RAM recommended)
   - Browser hardware acceleration
   - TensorFlow Lite optimization

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Detailed liveness results
result = detector.comprehensive_liveness_check(image)
print(f"Detailed result: {json.dumps(result, indent=2)}")
```

## Future Enhancements

### Planned Features
1. **Adaptive Thresholds**: Machine learning-based parameter tuning
2. **Behavioral Analysis**: Micro-expression detection
3. **Multi-Frame Analysis**: Temporal consistency checks
4. **Advanced Spoofing Detection**: IR and depth camera support

### Research Areas
1. **Continuous Authentication**: Real-time liveness monitoring
2. **Privacy-Preserving Detection**: Federated learning approaches
3. **Cross-Platform Optimization**: Native mobile implementations
4. **Accessibility Improvements**: Alternative verification methods

---

*This document is part of the Z-Secure platform documentation. For technical support, please refer to the main README or contact the development team.*
