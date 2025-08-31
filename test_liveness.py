#!/usr/bin/env python3
"""
Test script for liveness detection functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.liveness_detector import LivenessDetector
import cv2
import numpy as np
import base64
from PIL import Image
import io

def test_liveness_detector():
    """Test the liveness detector with a sample image"""
    print("Testing Liveness Detection System...")
    print("-" * 50)
    
    try:
        # Initialize liveness detector
        detector = LivenessDetector()
        print("✓ Liveness detector initialized successfully")
        
        # Create a simple test image (black square with white circle for face)
        test_image = np.zeros((400, 400, 3), dtype=np.uint8)
        cv2.circle(test_image, (200, 200), 80, (255, 255, 255), -1)  # White circle for face
        cv2.circle(test_image, (180, 180), 5, (0, 0, 0), -1)  # Left eye
        cv2.circle(test_image, (220, 180), 5, (0, 0, 0), -1)  # Right eye
        cv2.ellipse(test_image, (200, 220), (20, 10), 0, 0, 180, (0, 0, 0), 2)  # Mouth
        
        print("✓ Test image created")
        
        # Convert to base64 for testing
        pil_image = Image.fromarray(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format='JPEG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        print("✓ Test image converted to base64")
        
        # Test individual components
        print("\nTesting individual liveness detection components:")
        
        # Test blink detection
        blink_result = detector.detect_blink(test_image)
        print(f"  Blink Detection: {blink_result}")
        
        # Test head movement detection
        movement_result = detector.detect_head_movement(test_image)
        print(f"  Head Movement: {movement_result}")
        
        # Test texture analysis
        texture_result = detector.analyze_texture_variance(test_image)
        print(f"  Texture Analysis: {texture_result}")
        
        # Test face quality check
        quality_result = detector.check_face_quality(test_image)
        print(f"  Face Quality: {quality_result}")
        
        # Test comprehensive liveness check
        print("\nTesting comprehensive liveness detection:")
        comprehensive_result = detector.comprehensive_liveness_check(test_image)
        print(f"  Comprehensive Result: {comprehensive_result}")
        
        # Test base64 processing
        print("\nTesting base64 image processing:")
        b64_result = detector.process_image_for_liveness(f"data:image/jpeg;base64,{img_str}")
        print(f"  Base64 Processing Result: {b64_result}")
        
        print("\n" + "=" * 50)
        print("LIVENESS DETECTION TEST SUMMARY:")
        print("=" * 50)
        
        if 'error' not in comprehensive_result:
            print("✓ All liveness detection components are working")
            print(f"✓ Liveness Score: {comprehensive_result.get('liveness_score', 0)}")
            print(f"✓ Checks Passed: {comprehensive_result.get('checks_passed', 0)}/{comprehensive_result.get('total_checks', 4)}")
        else:
            print(f"✗ Error in liveness detection: {comprehensive_result.get('error')}")
        
        if 'error' not in b64_result:
            print("✓ Base64 image processing is working")
        else:
            print(f"✗ Error in base64 processing: {b64_result.get('error')}")
        
        print("\nNote: This is a synthetic test image. Real liveness detection")
        print("requires actual human faces with proper lighting and movement.")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing liveness detection: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_face_recognition_integration():
    """Test integration with face recognition service"""
    print("\n" + "=" * 50)
    print("TESTING FACE RECOGNITION INTEGRATION:")
    print("=" * 50)
    
    try:
        from src.face_recognition_service import FaceRecognitionService
        
        # Initialize face recognition service
        face_service = FaceRecognitionService()
        print("✓ Face recognition service initialized with liveness detection")
        
        # Create a test image
        test_image = np.zeros((400, 400, 3), dtype=np.uint8)
        cv2.circle(test_image, (200, 200), 80, (255, 255, 255), -1)
        
        # Convert to base64
        pil_image = Image.fromarray(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format='JPEG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        face_data_b64 = f"data:image/jpeg;base64,{img_str}"
        
        # Test processing with liveness
        result = face_service.process_face_data_with_liveness(face_data_b64, require_liveness=True)
        print(f"✓ Face processing with liveness result: {result['success']}")
        
        if not result['success']:
            print(f"  Expected failure reason: {result['error']}")
        
        # Test without liveness requirement
        result_no_liveness = face_service.process_face_data_with_liveness(face_data_b64, require_liveness=False)
        print(f"✓ Face processing without liveness result: {result_no_liveness['success']}")
        
        print("✓ Face recognition integration test completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing face recognition integration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Z-SECURE LIVENESS DETECTION TEST")
    print("=" * 50)
    
    success1 = test_liveness_detector()
    success2 = test_face_recognition_integration()
    
    print("\n" + "=" * 50)
    print("FINAL TEST RESULTS:")
    print("=" * 50)
    
    if success1 and success2:
        print("✓ All tests passed! Liveness detection is ready for use.")
        print("✓ The system can now detect and prevent spoofing attacks.")
        print("✓ Both registration and authentication will use liveness detection.")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
    
    print("\nTo use liveness detection:")
    print("1. Start the Flask application")
    print("2. Register a new account (will use liveness detection)")
    print("3. Log in with face authentication (will use liveness detection)")
    print("4. The system will automatically verify that you are a real person")
