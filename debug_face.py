#!/usr/bin/env python3
"""
Face Recognition Debug Script
Test the face recognition functionality independently
"""

import sys
import os
sys.path.insert(0, 'src')

from face_recognition_service import FaceRecognitionService
import base64

def test_face_recognition():
    """Test face recognition with sample data"""
    print("Testing Face Recognition Service...")
    
    face_service = FaceRecognitionService()
    
    # Test with a simple image (you would replace this with actual base64 data)
    # For testing, we'll create a dummy scenario
    
    print(f"Tolerance setting: {face_service.tolerance}")
    
    # Test processing
    print("\n1. Testing face processing...")
    # You would need actual base64 image data here for real testing
    
    print("\n2. Testing file operations...")
    test_user_id = "test_user_123"
    
    # Test save/load (with dummy data)
    import numpy as np
    dummy_encoding = np.random.rand(128)  # Face encodings are 128-dimensional
    
    # Test save
    save_result = face_service.save_face_encoding(test_user_id, dummy_encoding)
    print(f"Save encoding result: {save_result}")
    
    # Test load
    loaded_encoding = face_service.load_face_encoding(test_user_id)
    print(f"Load encoding result: {loaded_encoding is not None}")
    
    if loaded_encoding is not None:
        print(f"Loaded encoding shape: {loaded_encoding.shape}")
        print(f"Encodings match: {np.array_equal(dummy_encoding, loaded_encoding)}")
    
    # Cleanup
    try:
        os.remove(os.path.join('face_data', f'user_{test_user_id}.pkl'))
        print("Cleanup completed")
    except:
        pass
    
    print("\nFace recognition service test completed!")

def test_database_integration():
    """Test database integration"""
    print("\nTesting Database Integration...")
    
    try:
        from database_manager import DatabaseManager
        db_manager = DatabaseManager()
        
        # Test getting face encoding (will fail if no users exist)
        test_encoding = db_manager.get_face_encoding(1)
        print(f"Database face encoding test: {test_encoding is not None}")
        
    except Exception as e:
        print(f"Database test error: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("Face Recognition Debug Test")
    print("=" * 50)
    
    test_face_recognition()
    test_database_integration()
    
    print("\n" + "=" * 50)
    print("Debug test completed!")
    print("=" * 50)
