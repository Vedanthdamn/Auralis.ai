# Python 3.13.5 Compatibility Upgrade

## Overview
This document details the dependency changes made to ensure compatibility with Python 3.13.5.

## Problem
The original dependencies included:
- `tensorflow-macos==2.16.1` - Not available for Python 3.13
- `tensorflow-metal==1.1.0` - No longer needed
- `numpy==1.26.3` - Limited Python 3.13 support
- `scikit-learn==1.4.0` - Does not support Python 3.13
- `pandas==2.1.4` - Does not support Python 3.13

## Solution

### Key Changes

#### 1. TensorFlow Updates
- **Removed**: `tensorflow-macos` and `tensorflow-metal` (deprecated packages)
- **Added**: `tensorflow==2.18.0` (unified package with Apple Silicon support)
- **Reason**: Starting from TensorFlow 2.16+, Apple Silicon (M1/M2/M4) support is built into the main `tensorflow` package. The `tensorflow-macos` and `tensorflow-metal` packages are no longer maintained or needed.

#### 2. NumPy Update
- **Changed**: `numpy==1.26.3` → `numpy==2.1.0`
- **Reason**: NumPy 2.1.0 has full Python 3.13 support and provides better performance with modern Python versions.

#### 3. Scikit-learn Update
- **Changed**: `scikit-learn==1.4.0` → `scikit-learn==1.5.2`
- **Reason**: Version 1.5+ adds Python 3.13 support and includes important bug fixes.

#### 4. Pandas Update
- **Changed**: `pandas==2.1.4` → `pandas==2.2.3`
- **Reason**: Version 2.2+ adds Python 3.13 support and includes performance improvements.

### Files Updated

#### Requirements Files
1. **backend/requirements.txt**
   - Updated numpy, scikit-learn, tensorflow
   - Removed tensorflow-macos and tensorflow-metal

2. **ml_model/requirements.txt**
   - Updated numpy, pandas, scikit-learn, tensorflow
   - Removed tensorflow-macos and tensorflow-metal

3. **simulation/requirements.txt**
   - Updated numpy

#### Documentation Files
1. **README.md**
   - Updated Python version badge from 3.9+ to 3.13+
   - Updated prerequisites section
   - Updated Raspberry Pi deployment instructions

2. **PROJECT_SUMMARY.md**
   - Updated Python version requirement from 3.9+ to 3.13+

3. **docs/DEVELOPMENT.md**
   - Updated Python version prerequisite from 3.9+ to 3.13+
   - Updated version check instructions

4. **docs/FAQ.md**
   - Updated Python version requirement from 3.9+ to 3.13+

5. **docs/QUICKSTART.md**
   - Updated Python version prerequisite from 3.9+ to 3.13+
   - Updated troubleshooting section

## Installation Instructions

### For Python 3.13.5 users

1. **Clone the repository** (if not already done)
   ```bash
   git clone https://github.com/Vedanthdamn/Auralis.ai.git
   cd Auralis.ai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **ML Model Setup**
   ```bash
   cd ../ml_model
   pip install -r requirements.txt
   python generate_data.py
   python train_model.py
   ```

4. **Simulation Setup**
   ```bash
   cd ../simulation
   pip install -r requirements.txt
   ```

## Compatibility Notes

### Tested Platform
- Python 3.13.5
- macOS (Apple Silicon - M1/M2/M4)

### Expected to work on
- Python 3.13.x on any platform
- Linux (x86_64, ARM)
- Windows (x86_64)

### Apple Silicon Users
- No need for separate `tensorflow-macos` or `tensorflow-metal` packages
- TensorFlow 2.18.0 includes built-in Metal acceleration
- GPU acceleration works automatically when available

## Breaking Changes

### None Expected
All changes are backward compatible within the functionality scope:
- The updated packages maintain API compatibility
- Existing code does not require modifications
- Model training and inference work the same way
- All features remain functional

### Migration Notes
If you have an existing virtual environment with old dependencies:

1. **Option 1: Clean install (Recommended)**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Option 2: Upgrade in place**
   ```bash
   source venv/bin/activate
   pip install --upgrade -r requirements.txt
   ```

## Verification

After installation, verify everything works:

```bash
# Test imports
python3 -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python3 -c "import tensorflow; print(f'TensorFlow: {tensorflow.__version__}')"
python3 -c "import sklearn; print(f'scikit-learn: {sklearn.__version__}')"
python3 -c "import pandas; print(f'Pandas: {pandas.__version__}')"

# Should output:
# NumPy: 2.1.0
# TensorFlow: 2.18.0
# scikit-learn: 1.5.2
# Pandas: 2.2.3
```

## Troubleshooting

### Issue: Installation fails with compatibility errors
**Solution**: Ensure you're using Python 3.13.5 or higher:
```bash
python3 --version
```

### Issue: TensorFlow installation is slow
**Solution**: This is normal. TensorFlow is a large package and can take several minutes to download and install.

### Issue: Metal acceleration not working on Apple Silicon
**Solution**: Verify your setup:
```python
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
```

### Issue: Old model files cause errors
**Solution**: Retrain the model with the new dependencies:
```bash
cd ml_model
python generate_data.py
python train_model.py
```

## Performance Notes

### NumPy 2.x
- Improved performance for array operations
- Better memory efficiency
- Enhanced compatibility with modern Python

### TensorFlow 2.18
- Latest bug fixes and security updates
- Improved Apple Silicon support
- Better Python 3.13 compatibility

### Scikit-learn 1.5.2
- Performance improvements in tree-based models
- Better integration with NumPy 2.x
- Enhanced stability

## Future Compatibility

These dependency versions should remain stable for:
- Python 3.13.x releases
- Python 3.14 (when released, minor updates may be needed)

The project will continue to track stable releases of all dependencies to ensure long-term compatibility.

## References

- [TensorFlow Release Notes](https://github.com/tensorflow/tensorflow/releases)
- [NumPy Release Notes](https://numpy.org/news/)
- [Scikit-learn Release Notes](https://scikit-learn.org/stable/whats_new.html)
- [Pandas Release Notes](https://pandas.pydata.org/docs/whatsnew/index.html)

## Support

For issues related to this upgrade:
1. Check this document first
2. Review the main README.md
3. Check existing GitHub issues
4. Create a new issue with:
   - Python version (`python3 --version`)
   - Platform (macOS/Linux/Windows)
   - Error message
   - Steps to reproduce
