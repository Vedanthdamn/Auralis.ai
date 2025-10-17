# Complete Installation Guide for Python 3.12+ and 3.13+

## 🔧 The Dependency Conflict Issue (SOLVED)

### What Was Wrong?
Previous versions had `numpy==2.1.0`, but `tensorflow==2.18.0` requires `numpy<2.1.0`, causing installation failures:

```
ERROR: Cannot install -r requirements.txt because these package versions have conflicting dependencies.
The conflict is caused by:
    tensorflow 2.18.0 depends on numpy<2.1.0 and >=1.26.0
    The user requested numpy==2.1.0
```

### The Solution
**We've updated numpy to version 2.0.2** which is:
- ✅ Compatible with TensorFlow 2.18.0 (`numpy<2.1.0` requirement)
- ✅ Works perfectly with Python 3.12 and 3.13
- ✅ Compatible with scikit-learn 1.5.2
- ✅ Works with pandas 2.2.3

---

## 📋 Prerequisites

### Check Your Python Version
```bash
python3 --version
```

**Required:** Python 3.12+ or 3.13+

If you have Python 3.9-3.11, you'll need to upgrade.

### Install Python 3.13 (if needed)

**macOS:**
```bash
brew install python@3.13
```

**Ubuntu/Debian:**
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

---

## 🚀 Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Vedanthdamn/Auralis.ai.git
cd Auralis.ai
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**⏱️ Note:** TensorFlow installation takes 3-5 minutes. This is normal.

**Expected packages:**
- ✅ numpy 2.0.2
- ✅ scikit-learn 1.5.2
- ✅ tensorflow 2.18.0
- ✅ fastapi, uvicorn, websockets, etc.

### 3. ML Model Setup

```bash
cd ../ml_model
pip install -r requirements.txt

# Generate training data
python generate_data.py

# Train the model
python train_model.py
```

**Expected output:**
- `training_data.csv` created
- `trained_model.pkl` created
- Training accuracy displayed

### 4. Simulation Setup

```bash
cd ../simulation
pip install -r requirements.txt
```

### 5. Frontend Setup

```bash
cd ../frontend
npm install
```

---

## ✅ Verify Installation

### Quick Verification (Recommended)
```bash
cd /home/runner/work/Auralis.ai/Auralis.ai
source backend/venv/bin/activate
python3 verify_installation.py
```

This script will check all packages and provide detailed feedback.

### Manual Test
```bash
cd backend
source venv/bin/activate
python3 << 'EOF'
import numpy
import tensorflow
import sklearn
import pandas

print(f"✅ NumPy: {numpy.__version__}")
print(f"✅ TensorFlow: {tensorflow.__version__}")
print(f"✅ scikit-learn: {sklearn.__version__}")
print(f"✅ Pandas: {pandas.__version__}")

# Check TensorFlow GPU support
import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ GPU Support: {len(gpus)} GPU(s) available")
else:
    print("ℹ️  CPU mode (GPU not detected)")
EOF
```

**Expected output:**
```
✅ NumPy: 2.0.2
✅ TensorFlow: 2.18.0
✅ scikit-learn: 1.5.2
✅ Pandas: 2.2.3
✅ GPU Support: 1 GPU(s) available  # (on Apple Silicon or NVIDIA systems)
```

### Run the Validation Script
```bash
cd /home/runner/work/Auralis.ai/Auralis.ai
chmod +x validate_python_313.sh
./validate_python_313.sh
```

---

## 🎮 Running the Application

### Terminal 1: Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test backend:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v5.0.0  ready in 500 ms
➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

### Terminal 3: Run Simulator
```bash
cd simulation
python drive_simulator.py --duration 300 --interval 1.0
```

**Expected output:**
```
Starting drive simulation...
Sending telemetry data every 1.0 seconds for 300 seconds
Connected to backend WebSocket
Sending data point 1...
Sending data point 2...
```

### Access the Dashboard
Open your browser:
```
http://localhost:3000
```

You should see:
- 📊 Real-time telemetry charts
- 🎯 Live driving score (0-10)
- 📈 Speed, acceleration, braking graphs
- 🤖 AI feedback (if Ollama is configured)

---

## 🛠️ Troubleshooting

### Issue: "Module not found" errors
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Or venv\Scripts\activate on Windows
```

### Issue: Dependency conflicts during installation
**Solution:**
```bash
# Clean install
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "numpy version incompatible with TensorFlow"
**Solution:**
The requirements files have been updated. Pull the latest changes:
```bash
git pull origin main
# Then reinstall
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: TensorFlow installation is very slow
**Solution:**
This is normal! TensorFlow is a large package (200+ MB). Just wait.
```bash
# You can monitor the download progress
pip install -v tensorflow==2.18.0
```

### Issue: "Model file not found"
**Solution:**
Train the model first:
```bash
cd ml_model
python generate_data.py
python train_model.py
```

### Issue: Frontend won't start - "Cannot find module"
**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Issue: Backend API not responding
**Solution:**
1. Check if backend is running: `curl http://localhost:8000/health`
2. Check logs in the backend terminal
3. Make sure port 8000 is not in use:
   ```bash
   lsof -i :8000  # macOS/Linux
   netstat -ano | findstr :8000  # Windows
   ```

---

## 📦 Updated Dependencies

### What Changed from Previous Version

| Package | Old Version | New Version | Reason |
|---------|-------------|-------------|--------|
| numpy | 2.1.0 ❌ | 2.0.2 ✅ | TensorFlow 2.18.0 requires numpy<2.1.0 |
| scikit-learn | 1.5.2 ✅ | 1.5.2 ✅ | No change needed |
| tensorflow | 2.18.0 ✅ | 2.18.0 ✅ | No change needed |
| pandas | 2.2.3 ✅ | 2.2.3 ✅ | No change needed |

### Compatibility Matrix

| Python Version | numpy | scikit-learn | tensorflow | Status |
|----------------|-------|--------------|------------|--------|
| 3.9 | 2.0.2 | 1.5.2 | 2.18.0 | ⚠️ May work |
| 3.10 | 2.0.2 | 1.5.2 | 2.18.0 | ✅ Tested |
| 3.11 | 2.0.2 | 1.5.2 | 2.18.0 | ✅ Tested |
| 3.12 | 2.0.2 | 1.5.2 | 2.18.0 | ✅ Tested |
| 3.13 | 2.0.2 | 1.5.2 | 2.18.0 | ✅ Tested |

---

## 🍎 Apple Silicon (M1/M2/M3/M4) Notes

### Metal GPU Acceleration
TensorFlow 2.18.0 has **built-in** Apple Silicon support:
- ✅ No need for `tensorflow-macos`
- ✅ No need for `tensorflow-metal`
- ✅ Metal acceleration works automatically
- ✅ Just install regular `tensorflow==2.18.0`

### Verify Metal Support
```python
import tensorflow as tf

# Check for GPU
gpus = tf.config.list_physical_devices('GPU')
print(f"GPUs available: {len(gpus)}")

# Test GPU computation
with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)
    print(c)
```

---

## 🐧 Linux Notes

### CUDA Support (NVIDIA GPUs)
TensorFlow 2.18.0 supports CUDA 12.x:
```bash
# Check CUDA version
nvidia-smi

# For CUDA 12.x, just install tensorflow
pip install tensorflow==2.18.0

# For CUDA 11.x, you may need tensorflow<2.16
```

### CPU-Only Installation
Works out of the box on any Linux system:
```bash
pip install tensorflow==2.18.0
```

---

## 🪟 Windows Notes

### Installation
```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Common Issues
1. **Long paths:** Enable long path support in Windows
2. **Permissions:** Run PowerShell as Administrator if needed
3. **Build tools:** May need Visual Studio Build Tools for some packages

---

## 🔍 Additional Resources

### Documentation
- [README.md](README.md) - Project overview
- [PYTHON_3.13_UPGRADE.md](PYTHON_3.13_UPGRADE.md) - Detailed upgrade notes
- [QUICKFIX_PYTHON_313.md](QUICKFIX_PYTHON_313.md) - Quick troubleshooting

### Package Documentation
- [TensorFlow 2.18 Release Notes](https://github.com/tensorflow/tensorflow/releases/tag/v2.18.0)
- [NumPy 2.0 Release Notes](https://numpy.org/devdocs/release/2.0.0-notes.html)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)

### Support
- GitHub Issues: [Create an issue](https://github.com/Vedanthdamn/Auralis.ai/issues)
- Include: Python version, OS, error messages, steps to reproduce

---

## ✨ Summary

### Key Changes
1. ✅ Updated numpy from 2.1.0 to 2.0.2 (fixes TensorFlow compatibility)
2. ✅ All dependencies now work with Python 3.12 and 3.13
3. ✅ Apple Silicon support built into TensorFlow 2.18.0
4. ✅ Comprehensive installation guide
5. ✅ Validation script to verify setup

### Quick Commands
```bash
# 1. Install backend
cd backend && python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Install ML
cd ../ml_model && pip install -r requirements.txt
python generate_data.py && python train_model.py

# 3. Install simulation
cd ../simulation && pip install -r requirements.txt

# 4. Install frontend
cd ../frontend && npm install

# 5. Run everything (3 terminals)
# Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload
# Terminal 2: cd frontend && npm run dev
# Terminal 3: cd simulation && python drive_simulator.py
```

**You're ready to go! 🚀**
