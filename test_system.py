#!/usr/bin/env python3
"""
EncryptPro v2 - Installation and System Test
"""

import sys
import os
import subprocess

def test_python_version():
    """Test Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\nTesting dependencies...")
    dependencies = [
        'flask',
        'werkzeug', 
        'PIL',
        'numpy',
        'cryptography'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} - OK")
        except ImportError:
            print(f"✗ {dep} - Missing")
            all_ok = False
    
    return all_ok

def test_opencv():
    """Test OpenCV installation"""
    print("\nTesting OpenCV...")
    try:
        import cv2
        print(f"✓ OpenCV {cv2.__version__} - OK")
        return True
    except ImportError:
        print("✗ OpenCV - Missing")
        return False

def test_face_recognition():
    """Test face recognition library"""
    print("\nTesting face recognition...")
    try:
        import face_recognition
        print("✓ face_recognition - OK")
        return True
    except ImportError:
        print("✗ face_recognition - Missing")
        return False

def test_camera():
    """Test camera access"""
    print("\nTesting camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Camera access - OK")
                return True
            else:
                print("✗ Camera access - Cannot capture frame")
                return False
        else:
            print("✗ Camera access - Cannot open camera")
            return False
    except Exception as e:
        print(f"✗ Camera access - Error: {e}")
        return False

def test_directories():
    """Test required directories"""
    print("\nTesting directories...")
    directories = ['uploads', 'processed', 'face_data', 'templates', 'src']
    all_ok = True
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ {directory}/ - OK")
        else:
            print(f"✗ {directory}/ - Missing")
            all_ok = False
    
    return all_ok

def test_files():
    """Test required files"""
    print("\nTesting files...")
    files = ['app.py', 'requirements.txt', 'README.md', 'start.bat']
    all_ok = True
    
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file} - OK")
        else:
            print(f"✗ {file} - Missing")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 50)
    print("EncryptPro v2 - System Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_directories,
        test_files,
        test_dependencies,
        test_opencv,
        test_face_recognition,
        test_camera
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All tests passed ({passed}/{total})")
        print("\nEncryptPro v2 is ready to run!")
        print("Use 'start.bat' to launch the application.")
    else:
        print(f"✗ {total - passed} test(s) failed ({passed}/{total})")
        print("\nPlease fix the issues above before running EncryptPro v2.")
        
        if not test_dependencies():
            print("\nTo install dependencies:")
            print("pip install -r requirements.txt")

if __name__ == '__main__':
    main()
