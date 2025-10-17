#!/usr/bin/env python3
"""
Quick verification script to check if all dependencies are installed correctly.
Run this after installing the requirements to verify everything works.
"""

import sys
from typing import Tuple, List

def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is 3.12+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 12:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"❌ Python {version.major}.{version.minor}.{version.micro} (need 3.12+)"

def check_package(package_name: str, expected_version: str = None) -> Tuple[bool, str]:
    """Check if a package is installed and optionally verify version"""
    try:
        if package_name == 'sklearn':
            import sklearn as module
            display_name = 'scikit-learn'
        else:
            module = __import__(package_name)
            display_name = package_name
        
        version = getattr(module, '__version__', 'unknown')
        
        if expected_version:
            # Check major.minor version
            installed_major_minor = '.'.join(version.split('.')[:2])
            expected_major_minor = '.'.join(expected_version.split('.')[:2])
            
            if installed_major_minor == expected_major_minor:
                return True, f"✅ {display_name:15s} {version:10s}"
            else:
                return True, f"⚠️  {display_name:15s} {version:10s} (expected {expected_version}, but may work)"
        else:
            return True, f"✅ {display_name:15s} {version:10s}"
    except ImportError as e:
        return False, f"❌ {package_name:15s} NOT INSTALLED"

def check_tensorflow_gpu():
    """Check if TensorFlow GPU support is available"""
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            return True, f"✅ GPU Support: {len(gpus)} GPU(s) detected"
        else:
            return True, "ℹ️  CPU mode (no GPU detected - this is normal on many systems)"
    except Exception as e:
        return False, f"❌ TensorFlow GPU check failed: {str(e)}"

def main():
    print("=" * 60)
    print("DriveMind.ai - Installation Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    print("1. Checking Python Version")
    print("-" * 60)
    success, message = check_python_version()
    print(message)
    if not success:
        print("\n⚠️  Warning: Python 3.12+ is recommended")
    print()
    
    # Check required packages
    print("2. Checking Core Packages")
    print("-" * 60)
    packages = [
        ('numpy', '2.0.2'),
        ('pandas', '2.2.3'),
        ('sklearn', '1.5.2'),
        ('tensorflow', '2.18.0'),
    ]
    
    all_ok = True
    for package_name, expected_version in packages:
        success, message = check_package(package_name, expected_version)
        print(message)
        if not success:
            all_ok = False
    print()
    
    # Check additional packages
    print("3. Checking Additional Packages")
    print("-" * 60)
    additional_packages = [
        'fastapi',
        'uvicorn',
        'websockets',
        'requests',
        'joblib',
        'matplotlib'
    ]
    
    for package_name in additional_packages:
        success, message = check_package(package_name)
        print(message)
        if not success:
            print(f"   ℹ️  This package may not be needed in your current environment")
    print()
    
    # Check TensorFlow GPU support
    print("4. Checking TensorFlow GPU Support")
    print("-" * 60)
    success, message = check_tensorflow_gpu()
    print(message)
    print()
    
    # Final summary
    print("=" * 60)
    if all_ok:
        print("✅ All core packages installed successfully!")
        print()
        print("Next Steps:")
        print("1. Train the ML model:")
        print("   cd ml_model")
        print("   python generate_data.py")
        print("   python train_model.py")
        print()
        print("2. Start the backend:")
        print("   cd backend")
        print("   source venv/bin/activate")
        print("   uvicorn main:app --reload")
        print()
        print("3. Start the frontend:")
        print("   cd frontend")
        print("   npm run dev")
    else:
        print("❌ Some packages failed to import")
        print()
        print("To fix:")
        print("1. Make sure virtual environment is activated:")
        print("   source venv/bin/activate")
        print()
        print("2. Install missing packages:")
        print("   pip install -r requirements.txt")
        print()
        print("3. If problems persist, try a clean install:")
        print("   rm -rf venv")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
