#!/usr/bin/env python3
"""
Test script for the Screenshot Service application
"""

import os
import sys
import time
from datetime import datetime

def test_screenshot_capture():
    """Test the screenshot capture functionality"""
    
    print("Testing Screenshot Service...")
    print("=" * 40)
    
    # Test 1: Check if required modules can be imported
    print("1. Testing module imports...")
    try:
        from screenshot_app import ScreenshotCapture
        print("   ✓ ScreenshotCapture imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import ScreenshotCapture: {e}")
        return False
    
    # Test 2: Test screenshot directory creation
    print("2. Testing screenshot directory creation...")
    try:
        capture = ScreenshotCapture()
        if os.path.exists(capture.screenshot_dir):
            print(f"   ✓ Screenshot directory exists: {capture.screenshot_dir}")
        else:
            print(f"   ✗ Screenshot directory not found: {capture.screenshot_dir}")
            return False
    except Exception as e:
        print(f"   ✗ Failed to create ScreenshotCapture: {e}")
        return False
    
    # Test 3: Test full screenshot capture
    print("3. Testing full screenshot capture...")
    try:
        filepath = capture.take_full_screenshot()
        if filepath and os.path.exists(filepath):
            print(f"   ✓ Full screenshot saved: {os.path.basename(filepath)}")
            # Clean up test file
            os.remove(filepath)
            print("   ✓ Test file cleaned up")
        else:
            print("   ✗ Full screenshot failed")
            return False
    except Exception as e:
        print(f"   ✗ Full screenshot error: {e}")
        return False
    
    # Test 4: Test PyQt6 imports (for GUI components)
    print("4. Testing PyQt6 imports...")
    try:
        from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
        from PyQt6.QtCore import QThread, pyqtSignal
        print("   ✓ PyQt6 components imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import PyQt6: {e}")
        return False
    
    # Test 5: Test keyboard module
    print("5. Testing keyboard module...")
    try:
        import keyboard
        print("   ✓ Keyboard module imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import keyboard: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("All tests passed! The application should work correctly.")
    print("\nTo run the application:")
    print("1. python screenshot_app.py")
    print("2. Or build the executable: python build.py")
    return True

def test_build_process():
    """Test the build process"""
    print("\nTesting build process...")
    print("=" * 40)
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("✓ PyInstaller is available")
    except ImportError:
        print("✗ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check if all required files exist
    required_files = ['screenshot_app.py', 'requirements.txt', 'build.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} not found")
            return False
    
    print("✓ Build process should work correctly")
    return True

if __name__ == "__main__":
    print("Screenshot Service Test Suite")
    print("=" * 50)
    
    success = test_screenshot_capture()
    build_success = test_build_process()
    
    if success and build_success:
        print("\n🎉 All tests passed! Your application is ready to use.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1) 