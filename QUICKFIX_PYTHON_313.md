# Quick Start Guide for Python 3.13.5

## The Problem You Had
You were getting errors:
```
ERROR: Could not find a version that satisfies the requirement tensorflow-macos==2.16.1
```

This is because `tensorflow-macos` is **no longer available** and is not needed for Python 3.13.5.

## The Solution
All dependencies have been updated to work with Python 3.13.5!

## Quick Setup (3 Steps)

### Step 1: Install Backend Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Install ML Model Dependencies & Train Model
```bash
cd ../ml_model
pip install -r requirements.txt
python generate_data.py
python train_model.py
```

### Step 3: Install Simulation Dependencies
```bash
cd ../simulation
pip install -r requirements.txt
```

## Verify Installation
Run the validation script:
```bash
chmod +x validate_python_313.sh
./validate_python_313.sh
```

This will check:
- ✅ Python version is 3.13+
- ✅ All packages are installed correctly
- ✅ Versions match requirements
- ✅ TensorFlow Metal support (on macOS)

## What Changed?

### Old Dependencies (Didn't work on Python 3.13.5)
```
numpy==1.26.3
scikit-learn==1.4.0
tensorflow-macos==2.16.1  ❌ Not available
tensorflow-metal==1.1.0    ❌ Not available
tensorflow==2.16.1
pandas==2.1.4
```

### New Dependencies (Works on Python 3.13.5)
```
numpy==2.1.0              ✅ Python 3.13 support
scikit-learn==1.5.2       ✅ Python 3.13 support
tensorflow==2.18.0        ✅ Includes Apple Silicon support
pandas==2.2.3             ✅ Python 3.13 support
```

## Important Notes

### For macOS Users (Apple Silicon - M1/M2/M4)
- **You don't need `tensorflow-macos` anymore!**
- TensorFlow 2.18.0 has built-in Apple Silicon support
- Metal GPU acceleration is automatic
- Everything just works™

### Why TensorFlow 2.18.0?
- Full Python 3.13 support
- Built-in Apple Silicon/Metal support
- Latest security updates
- Better performance

### Why NumPy 2.1.0?
- Python 3.13 support
- Better performance
- Enhanced compatibility

## Run the Application

After installation, start all services:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm run dev
```

**Terminal 3 - Simulator:**
```bash
cd simulation
python drive_simulator.py --duration 300
```

**Open Browser:**
```
http://localhost:3000
```

## Troubleshooting

### "Module not found" errors
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Installation is slow
This is normal! TensorFlow 2.18.0 is a large package (200+ MB). Be patient, it will finish.

### Old virtual environment issues
If you have an old venv, delete it and start fresh:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Need to retrain model
If you get model errors:
```bash
cd ml_model
python generate_data.py
python train_model.py
```

## Need More Help?

1. **Detailed Guide**: Read `PYTHON_3.13_UPGRADE.md`
2. **Validation**: Run `./validate_python_313.sh`
3. **Full Docs**: Check `README.md` and `docs/` folder
4. **Issues**: Open a GitHub issue with error details

## Summary

✅ All dependencies updated for Python 3.13.5
✅ No more `tensorflow-macos` needed
✅ Apple Silicon support built-in
✅ All documentation updated
✅ Validation script included

**Just follow the 3 setup steps above and you're good to go!** 🚀
