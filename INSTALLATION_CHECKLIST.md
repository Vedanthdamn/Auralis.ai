# Installation Checklist ✅

Use this as a quick reference while installing. Check off each item as you complete it.

## Prerequisites

- [ ] Python 3.12+ or 3.13 installed
  ```bash
  python3 --version
  ```

- [ ] Node.js 18+ installed (for frontend)
  ```bash
  node --version
  ```

- [ ] Git installed
  ```bash
  git --version
  ```

---

## Backend Setup

- [ ] Navigate to backend directory
  ```bash
  cd backend
  ```

- [ ] Create virtual environment
  ```bash
  python3 -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ```

- [ ] Upgrade pip
  ```bash
  pip install --upgrade pip
  ```

- [ ] Install requirements (takes 3-5 minutes)
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify backend packages
  ```bash
  pip list | grep -E "numpy|tensorflow|scikit"
  # Should show: numpy 2.0.2, tensorflow 2.18.0, scikit-learn 1.5.2
  ```

---

## ML Model Setup

- [ ] Navigate to ml_model directory
  ```bash
  cd ../ml_model
  ```

- [ ] Install ML requirements
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Generate training data
  ```bash
  python generate_data.py
  ```
  **Expected:** `training_data.csv` created

- [ ] Train the model
  ```bash
  python train_model.py
  ```
  **Expected:** `trained_model.pkl` created, training stats displayed

---

## Simulation Setup

- [ ] Navigate to simulation directory
  ```bash
  cd ../simulation
  ```

- [ ] Install simulation requirements
  ```bash
  pip install -r requirements.txt
  ```

---

## Frontend Setup

- [ ] Navigate to frontend directory
  ```bash
  cd ../frontend
  ```

- [ ] Install npm packages
  ```bash
  npm install
  ```

---

## Verification

- [ ] Run verification script
  ```bash
  cd ..
  python3 verify_installation.py
  ```
  **Expected:** All ✅ green checkmarks

- [ ] Check backend health (Terminal 1)
  ```bash
  cd backend
  source venv/bin/activate
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
  Then in another terminal:
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status":"healthy"}
  ```

- [ ] Check frontend dev server (Terminal 2)
  ```bash
  cd frontend
  npm run dev
  # Should show: Local: http://localhost:3000/
  ```

- [ ] Run simulator (Terminal 3)
  ```bash
  cd simulation
  python drive_simulator.py --duration 60
  # Should connect and send data
  ```

- [ ] Open browser and check dashboard
  ```
  http://localhost:3000
  # Should show real-time charts and data
  ```

---

## Optional: Supabase Setup

- [ ] Create Supabase account at [supabase.com](https://supabase.com)

- [ ] Create new project

- [ ] Run database schema from `docs/database_schema.md`

- [ ] Copy `.env.example` to `.env`
  ```bash
  cd backend
  cp .env.example .env
  ```

- [ ] Add Supabase credentials to `.env`
  ```
  SUPABASE_URL=your_project_url
  SUPABASE_KEY=your_anon_key
  ```

---

## Optional: Ollama Setup (AI Feedback)

- [ ] Install Ollama from [ollama.ai](https://ollama.ai)

- [ ] Pull a model
  ```bash
  ollama pull llama2
  ```

- [ ] Start Ollama service
  ```bash
  ollama serve
  ```

- [ ] Verify Ollama is running
  ```bash
  curl http://localhost:11434/api/tags
  # Should return list of installed models
  ```

---

## Troubleshooting

If anything fails:

- [ ] Check you're in the right directory
- [ ] Check virtual environment is activated (`which python` should show venv path)
- [ ] Try clean install:
  ```bash
  cd backend
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

---

## Success! 🎉

If all items are checked, you're ready to use DriveMind.ai!

**To run the full application:**

1. **Terminal 1:** `cd backend && source venv/bin/activate && uvicorn main:app --reload`
2. **Terminal 2:** `cd frontend && npm run dev`
3. **Terminal 3:** `cd simulation && python drive_simulator.py`
4. **Browser:** Open `http://localhost:3000`

---

## Quick Reference

| Component | Port | Command |
|-----------|------|---------|
| Backend API | 8000 | `uvicorn main:app --reload` |
| Frontend | 3000 | `npm run dev` |
| Ollama (optional) | 11434 | `ollama serve` |

| File | Purpose |
|------|---------|
| `trained_model.pkl` | Trained ML model |
| `training_data.csv` | Generated training data |
| `.env` | Backend configuration |

---

**Need help?** Check [START_HERE.md](START_HERE.md) or [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
