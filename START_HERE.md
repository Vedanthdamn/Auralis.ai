# 🚀 START HERE - Python 3.13 Installation

## ✅ The Problem is FIXED!

Your dependency issue has been **completely resolved**. Here's what happened and how to install.

---

## 🔍 What Was Wrong?

You were getting this error:
```
ERROR: Cannot install tensorflow==2.18.0 and numpy==2.1.0
tensorflow 2.18.0 depends on numpy<2.1.0
```

**Root cause:** TensorFlow 2.18.0 requires numpy version **less than 2.1.0**, but the requirements specified numpy **2.1.0**.

---

## ✅ The Fix

We changed one line in all requirements files:
```diff
- numpy==2.1.0
+ numpy==2.0.2
```

**Why this works:**
- ✅ numpy 2.0.2 satisfies TensorFlow's requirement (`numpy<2.1.0`)
- ✅ numpy 2.0.2 works perfectly with Python 3.13
- ✅ numpy 2.0.2 is compatible with scikit-learn 1.5.2
- ✅ Everything else stays the same

---

## 📥 How to Install (Step by Step)

### Prerequisites
Make sure you have Python 3.12+ or 3.13:
```bash
python3 --version
# Should show: Python 3.12.x or 3.13.x
```

### Step 1: Get the Latest Code
If you already cloned the repo, pull the latest changes:
```bash
cd Auralis.ai
git pull origin main
```

If you haven't cloned yet:
```bash
git clone https://github.com/Vedanthdamn/Auralis.ai.git
cd Auralis.ai
```

### Step 2: Install Backend Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**⏱️ This takes 3-5 minutes** - TensorFlow is a large package, be patient!

### Step 3: Install ML Model Dependencies
```bash
cd ../ml_model
pip install -r requirements.txt
```

### Step 4: Generate Data and Train Model
```bash
python generate_data.py
python train_model.py
```

### Step 5: Install Simulation Dependencies
```bash
cd ../simulation
pip install -r requirements.txt
```

### Step 6: Verify Everything Works
```bash
cd ..
python3 verify_installation.py
```

You should see:
```
✅ Python 3.13.x
✅ NumPy: 2.0.2
✅ TensorFlow: 2.18.0
✅ scikit-learn: 1.5.2
✅ All core packages installed successfully!
```

---

## 🎮 Run the Application

Now you're ready to run the app!

### Terminal 1: Backend Server
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm install  # First time only
npm run dev
```

### Terminal 3: Driving Simulator
```bash
cd simulation
python drive_simulator.py --duration 300
```

### Open Your Browser
```
http://localhost:3000
```

You should see the dashboard with real-time driving data! 🎉

---

## 🆘 Troubleshooting

### "Module not found: numpy/tensorflow/sklearn"
**Solution:** Activate the virtual environment
```bash
source venv/bin/activate
```

### "Still getting dependency conflicts"
**Solution:** Clean install
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### "Installation takes too long"
**Solution:** This is normal! TensorFlow is 200+ MB. It will finish, just wait.

### "Python version too old"
**Solution:** Upgrade to Python 3.12 or 3.13
- **macOS:** `brew install python@3.13`
- **Ubuntu:** `sudo apt install python3.13`
- **Windows:** Download from [python.org](https://python.org)

---

## 📚 More Help

- **Quick Guide:** [PYTHON_313_QUICK_START.md](PYTHON_313_QUICK_START.md)
- **Detailed Guide:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Technical Details:** [PYTHON_3.13_UPGRADE.md](PYTHON_3.13_UPGRADE.md)
- **Main README:** [README.md](README.md)

---

## 📊 What Changed

| File | Change |
|------|--------|
| `backend/requirements.txt` | numpy 2.1.0 → 2.0.2 |
| `ml_model/requirements.txt` | numpy 2.1.0 → 2.0.2 |
| `simulation/requirements.txt` | numpy 2.1.0 → 2.0.2 |
| All other packages | No changes |

---

## ✨ Summary

1. ✅ The numpy/TensorFlow conflict is **fixed**
2. ✅ All dependencies work with Python 3.12 and 3.13
3. ✅ Installation is now straightforward
4. ✅ Comprehensive documentation provided
5. ✅ Verification script included

**Just follow the installation steps above and you're ready to go!** 🚀

---

## 💬 Still Need Help?

Open a GitHub issue with:
1. Your Python version: `python3 --version`
2. Your operating system (macOS/Linux/Windows)
3. The exact error message you're seeing
4. Output of: `pip list | grep -E "numpy|tensorflow|sklearn"`

We'll help you get it working! 😊
