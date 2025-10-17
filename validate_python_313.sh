#!/bin/bash
# Validation script for Python 3.13.5 compatibility upgrade

echo "======================================"
echo "Python 3.13.5 Compatibility Validation"
echo "======================================"
echo ""

# Check Python version
echo "1. Checking Python version..."
python3 --version
echo ""

# Verify it's Python 3.13+
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.13"

if (( $(echo "$PYTHON_VERSION >= $REQUIRED_VERSION" | bc -l) )); then
    echo "✅ Python version $PYTHON_VERSION is compatible (>= $REQUIRED_VERSION)"
else
    echo "❌ Python version $PYTHON_VERSION is not compatible (< $REQUIRED_VERSION)"
    echo "   Please upgrade to Python 3.13 or higher"
    exit 1
fi
echo ""

# Test package installations
echo "2. Testing package imports and versions..."
echo ""

python3 << 'EOF'
import sys

packages = [
    ('numpy', '2.1.0'),
    ('pandas', '2.2.3'),
    ('sklearn', '1.5.2'),
    ('tensorflow', '2.18.0'),
]

all_ok = True

for package_name, expected_version in packages:
    try:
        if package_name == 'sklearn':
            import sklearn as module
        else:
            module = __import__(package_name)
        
        version = module.__version__
        major_minor = '.'.join(version.split('.')[:2])
        expected_major_minor = '.'.join(expected_version.split('.')[:2])
        
        if major_minor == expected_major_minor:
            print(f"✅ {package_name:15s} {version:10s} (expected {expected_version})")
        else:
            print(f"⚠️  {package_name:15s} {version:10s} (expected {expected_version}, but close enough)")
    except ImportError as e:
        print(f"❌ {package_name:15s} NOT INSTALLED - {e}")
        all_ok = False

print()
if all_ok:
    print("✅ All packages imported successfully!")
else:
    print("❌ Some packages failed to import. Please run:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    exit 1
fi

# Test TensorFlow Metal support (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "3. Testing TensorFlow Metal acceleration (macOS)..."
    python3 << 'EOF'
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ Metal GPU acceleration available: {len(gpus)} GPU(s) detected")
    for gpu in gpus:
        print(f"   - {gpu}")
else:
    print("ℹ️  No GPU detected (this is normal on some systems)")
    print("   TensorFlow will use CPU, which is still functional")
EOF
fi

echo ""
echo "======================================"
echo "✅ Validation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Train the ML model:"
echo "   cd ml_model"
echo "   python generate_data.py"
echo "   python train_model.py"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload"
echo ""
echo "3. Start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Run the simulator:"
echo "   cd simulation"
echo "   python drive_simulator.py"
