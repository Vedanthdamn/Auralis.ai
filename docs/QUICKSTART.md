# DriveMind.ai Quick Start Guide

This guide will help you get DriveMind.ai up and running quickly.

## Prerequisites Check

Before starting, make sure you have:
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.13+ installed (`python3 --version`)
- [ ] Git installed (`git --version`)

## Quick Setup (5 minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Make setup script executable
chmod +x scripts/setup.sh

# Run setup
./scripts/setup.sh
```

This will:
1. Install all frontend dependencies
2. Create Python virtual environment
3. Install all backend dependencies
4. Generate training data
5. Train the ML model
6. Setup simulation environment

### Option 2: Manual Setup

#### 1. Frontend
```bash
cd frontend
npm install
```

#### 2. Backend
```bash
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

#### 3. ML Model
```bash
cd ../ml_model
pip install -r requirements.txt
python generate_data.py
python train_model.py
```

#### 4. Simulation
```bash
cd ../simulation
pip install -r requirements.txt
```

## Running the System

You'll need 3 terminal windows:

### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Wait for: `✅ Services initialized successfully`

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:3000/`

### Terminal 3: Simulation
```bash
cd simulation
python drive_simulator.py --duration 300
```

## Accessing the Dashboard

Open your browser and go to:
```
http://localhost:3000
```

You should see:
- ✅ Connection indicator showing "Connected"
- 📊 Charts updating in real-time
- 🎯 Live driving score
- 💬 AI feedback panel

## Testing the System

1. **Watch the simulation**: Terminal 3 will show driving data being sent
2. **Observe the dashboard**: Charts should update every second
3. **Check the score**: Should change based on driving behavior
4. **Read feedback**: AI-generated suggestions appear periodically

## Optional: Advanced Features

### Enable Supabase (Database)

1. Create account at https://supabase.com
2. Create a new project
3. Run SQL from `docs/database_schema.md`
4. Update `backend/.env`:
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   ```
5. Restart backend

### Enable Ollama (AI Feedback)

1. Install Ollama from https://ollama.ai
2. Run:
   ```bash
   ollama pull llama2
   ollama serve
   ```
3. Restart backend (it will auto-detect Ollama)

## Troubleshooting

### Frontend won't connect
- Check backend is running on port 8000
- Check WebSocket URL in browser console

### Backend crashes
- Ensure virtual environment is activated
- Check Python version is 3.13+
- Verify all dependencies installed

### No AI feedback
- This is normal if Ollama is not installed
- System falls back to rule-based feedback

### Model training fails
- Ensure you ran `generate_data.py` first
- Check you have enough disk space
- On macOS, TensorFlow Metal may need updates

## Next Steps

- Customize the simulation scenarios
- Modify scoring algorithm
- Add more telemetry metrics
- Deploy to production
- Integrate with real vehicle sensors

## Need Help?

- Check the main README.md
- Review the code comments
- Open an issue on GitHub
- Check logs in terminal windows
