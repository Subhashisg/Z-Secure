#!/usr/bin/env python3
"""
Test script for delete account functionality
"""

import sys
sys.path.insert(0, 'src')

from database_manager import DatabaseManager
import os

def test_delete_account_functionality():
    """Test the delete account feature"""
    print("Testing Delete Account Functionality")
    print("=" * 50)
    
    # Initialize database manager
    db = DatabaseManager()
    
    # Create a test user (if not exists)
    test_email = "test_delete@example.com"
    test_password = "testpassword123"
    
    # Check if test user exists
    if db.user_exists(test_email):
        print(f"Test user {test_email} already exists")
        # Get user ID
        user = db.verify_user_credentials(test_email, test_password)
        if user:
            user_id = user['id']
        else:
            print("Could not verify test user credentials")
            return
    else:
        print(f"Creating test user: {test_email}")
        # Create a dummy face encoding for testing
        import numpy as np
        dummy_face_encoding = np.random.rand(128)  # 128-dimensional face encoding
        
        user_id = db.create_user(test_email, test_password, dummy_face_encoding)
        if not user_id:
            print("Failed to create test user")
            return
        print(f"Created test user with ID: {user_id}")
    
    # Create test face data file
    face_file_path = f"face_data/user_{user_id}.pkl"
    if not os.path.exists(face_file_path):
        print(f"Creating test face data file: {face_file_path}")
        import pickle
        import numpy as np
        with open(face_file_path, 'wb') as f:
            pickle.dump(np.random.rand(128), f)
    
    # Test data existence before deletion
    print(f"\nBefore deletion:")
    user_data = db.get_user(user_id)
    print(f"- User exists: {user_data is not None}")
    print(f"- Face file exists: {os.path.exists(face_file_path)}")
    
    face_data = db.get_face_data(user_id)
    print(f"- Face data in DB: {face_data is not None}")
    
    # Test cleanup function
    print(f"\nTesting file cleanup...")
    cleanup_result = db.cleanup_user_files(user_id)
    print(f"- File cleanup result: {cleanup_result}")
    print(f"- Face file exists after cleanup: {os.path.exists(face_file_path)}")
    
    # Test account deletion
    print(f"\nTesting account deletion...")
    deletion_result = db.delete_user_account(user_id)
    print(f"- Account deletion result: {deletion_result}")
    
    # Test data existence after deletion
    print(f"\nAfter deletion:")
    user_data = db.get_user(user_id)
    print(f"- User exists: {user_data is not None}")
    
    face_data = db.get_face_data(user_id)
    print(f"- Face data in DB: {face_data is not None}")
    
    print(f"\n✅ Delete account functionality test completed!")

if __name__ == "__main__":
    test_delete_account_functionality()
