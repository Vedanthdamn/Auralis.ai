# DriveMind.ai 🚗

**AI-Powered Driver Safety Scoring System**

Illuminating Safer Journeys with AI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-61dafb.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)

---

> ## 🔧 Python 3.13 Installation Fixed! ✅
> 
> **Dependency conflicts resolved!** Installation now works smoothly on Python 3.12 and 3.13.
> 
> ### 📖 Installation Guides (Pick One)
> 
> 1. **[START_HERE.md](START_HERE.md)** ← **Best place to start!** Quick explanation + step-by-step
> 2. **[PYTHON_313_QUICK_START.md](PYTHON_313_QUICK_START.md)** ← 3-step quick start
> 3. **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** ← Comprehensive guide with troubleshooting
> 
> **What was fixed:** Updated numpy from 2.1.0 → 2.0.2 for TensorFlow 2.18.0 compatibility.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

DriveMind.ai is a comprehensive, full-stack driver safety scoring system that uses machine learning to analyze driving behavior in real-time. The system processes telemetry data (speed, acceleration, braking, steering) and provides:

- **Real-time safety scoring** (0-10 scale)
- **AI-generated driving feedback** (via local LLM integration)
- **Beautiful, responsive dashboard** with live charts
- **Data persistence** with Supabase
- **Realistic driving simulation** for testing

Perfect for:
- Driver training programs
- Fleet management
- Insurance telematics
- Research and development
- Personal driving improvement

---

## ✨ Features

### Personal Dashboard
- 📊 Real-time charts for speed, acceleration, and braking
- 🎯 Live driving score display with animated gauge
- 🤖 AI-generated feedback panel
- 🌓 Dark mode toggle with persistent preferences
- 📱 Fully responsive design
- ✨ Smooth animations with Framer Motion
- 🎨 Beautiful UI with TailwindCSS

### Fleet Dashboard (NEW!)
- 🚕 Multi-driver/vehicle tracking for fleet operators
- 🏆 Driver rankings and leaderboard
- 📈 Fleet-level statistics and insights
- 🤖 AI-powered per-driver feedback using Mistral 7B
- 📊 Performance trends and comparisons
- 🎯 Identify top performers and drivers needing training
- 🔄 Real-time data refresh (30s intervals)
- 🌓 Full dark mode support

### Backend (FastAPI)
- 🚀 High-performance async API
- 🔌 WebSocket support for real-time data streaming
- 🧠 ML inference for safety scoring
- 🤖 Optional Ollama LLM integration for feedback (Mistral 7B)
- 💾 Supabase database integration
- 📝 Comprehensive API documentation
- ✅ Request validation with Pydantic
- 🚗 Fleet management endpoints

### Machine Learning
- 🎓 Trained models using scikit-learn or TensorFlow
- 🍎 Optimized for Apple Silicon (M1/M2/M4) with Metal acceleration
- 📈 Multiple model types (Random Forest, Gradient Boosting, Neural Networks)
- 🎯 High accuracy safety score predictions
- 📊 Synthetic data generation for training

### Simulation
- 🚗 Realistic driving behavior simulation
- 🎭 Multiple driving scenarios (normal, highway, aggressive, cautious, emergency)
- 📡 Real-time telemetry transmission to backend
- ⚙️ Configurable parameters
- 🚕 **NEW**: Dual simulation modes (personal and fleet) that run independently
- 🔄 **NEW**: Concurrent simulation support - run multiple terminals simultaneously
- ⚡ **NEW**: Optimized for 1-second update intervals without timeouts

---

## 🏗️ Architecture

```
┌──────────────────┐   /ws/personal    ┌──────────────────┐
│ Personal         │◄─────────────────►│                  │
│ Dashboard        │                    │                  │
│ (Port 3000)      │                    │                  │
└──────────────────┘                    │  FastAPI Backend │
                                        │   (Port 8000)    │
┌──────────────────┐   /ws/fleet       │                  │
│ Fleet            │◄─────────────────►│  - /ws/personal  │
│ Dashboard        │                    │  - /ws/fleet     │
│ (Port 3000)      │                    │  - /ws (legacy)  │
└──────────────────┘                    └──────────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────┐
                    │                         │                     │
            ┌───────▼──────┐         ┌────────▼────────┐   ┌───────▼──────┐
            │  ML Service  │         │ Supabase Service│   │Ollama (opt.) │
            │  (Scoring)   │         │   (Database)    │   │   (LLM)      │
            └──────────────┘         └─────────────────┘   └──────────────┘
                    ▲
                    │
            ┌───────┴──────────┐
            │  Simulators      │
            │  --mode personal │
            │  --mode fleet    │
            └──────────────────┘
```

**Key Architecture Features:**
- **Parallel WebSocket Streams**: Separate endpoints ensure no data crosstalk
- **Independent Connection Pools**: Personal and fleet connections are isolated
- **Automatic Routing**: Backend routes data based on simulation mode
- **Backward Compatible**: Legacy `/ws` endpoint still supported

---

## 📦 Prerequisites

### Required
- **Node.js** 18+ (for frontend)
- **Python** 3.13+ (for backend and ML)
- **macOS** (recommended) or Linux/Windows

### Optional
- **Ollama** (for AI-generated feedback) - Install from [ollama.ai](https://ollama.ai)
- **Supabase** account (for data persistence) - Sign up at [supabase.com](https://supabase.com)

---

## 🚀 Installation

> **🎉 Python 3.13 Users:** Installation issues are **FIXED**! See [PYTHON_313_QUICK_START.md](PYTHON_313_QUICK_START.md) for the quick guide.
> 
> **📚 Comprehensive Guide:** For detailed installation instructions and troubleshooting, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md).
> 
> **Key Fix:** Updated numpy to 2.0.2 for full Python 3.12/3.13 compatibility with TensorFlow 2.18.0.

### 1. Clone the Repository

```bash
git clone https://github.com/Vedanthdamn/Auralis.ai.git
cd Auralis.ai
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. Backend Setup

```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. ML Model Setup

```bash
cd ../ml_model
pip install -r requirements.txt

# Generate training data
python generate_data.py

# Train the model
python train_model.py
```

### 5. Simulation Setup

```bash
cd ../simulation
pip install -r requirements.txt
```

### 6. Configure Environment Variables

```bash
cd ../backend
cp .env.example .env
# Edit .env with your Supabase credentials (optional)
```

---

## 🎮 Usage

### Quick Start (All Services)

#### Terminal 1: Start Backend
```bash
cd backend
source venv/bin/activate  # If not already activated
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

#### Terminal 3: Run Personal Simulation
```bash
cd simulation
python drive_simulator.py --duration 300 --interval 1.0 --mode personal
```

#### Terminal 4 (Optional): Run Fleet Simulation
```bash
cd simulation
python drive_simulator.py --duration 300 --interval 1.0 --mode fleet
```

**Note**: You can run multiple simulators simultaneously! Each terminal runs independently without interfering with the other.

### Access the Dashboards

#### Personal Dashboard
Open your browser and navigate to:
```
http://localhost:3000/dashboard
```

You should see:
- Real-time telemetry charts updating
- Live driving score
- AI-generated feedback (if Ollama is configured)

#### Fleet Dashboard
For fleet operators managing multiple drivers:
```
http://localhost:3000/dashboard/fleet
```

You should see:
- Fleet statistics (total drivers, trips, average score)
- Driver rankings and leaderboard
- AI-generated fleet insights
- Individual driver performance cards

**Note**: The fleet dashboard requires database setup and sample data. See [Fleet Dashboard Guide](docs/FLEET_DASHBOARD.md) for setup instructions.

### Quick Fleet Dashboard Setup

```bash
# Terminal 4: Generate sample fleet data (optional)
cd scripts
python generate_fleet_data.py --drivers 5 --sessions 10
```

This will create 5 sample drivers with 10 trips each to populate the fleet dashboard.

---

## 🚗 Simulation Modes

DriveMind.ai now supports two independent simulation modes that can run concurrently with **parallel WebSocket streaming**:

### Personal Mode (`--mode personal`)
- **Purpose**: Individual driver testing and training
- **Use Case**: Personal driving improvement, training scenarios
- **Icon**: 🚗
- **WebSocket Endpoint**: `ws://localhost:8000/ws/personal`
- **Dashboard URL**: `http://localhost:3000/dashboard`

### Fleet Mode (`--mode fleet`)
- **Purpose**: Fleet management and multi-vehicle monitoring
- **Use Case**: Fleet operators (Uber, Ola, delivery services)
- **Icon**: 🚕
- **WebSocket Endpoint**: `ws://localhost:8000/ws/fleet`
- **Dashboard URL**: `http://localhost:3000/dashboard/fleet`

### Key Features
- ✅ **Parallel WebSocket Streaming**: Dedicated endpoints for each dashboard
- ✅ **Independent Sessions**: Each mode maintains its own session ID and statistics
- ✅ **Concurrent Execution**: Run both modes simultaneously without interference
- ✅ **No Data Crosstalk**: Personal and fleet data streams are completely isolated
- ✅ **Retry Mechanism**: Automatic retry with exponential backoff on failures
- ✅ **High-Frequency Updates**: Support for 1-second update intervals
- ✅ **Concurrency Control**: Backend handles up to 10 simultaneous requests
- ✅ **Graceful Degradation**: Partial responses when backend is overloaded

---

### Running Both Dashboards in Parallel

You can run both personal and fleet dashboards simultaneously with live data streaming to each:

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Personal Simulation
cd simulation
python drive_simulator.py --duration 600 --interval 1.0 --mode personal

# Terminal 4: Fleet Simulation
cd simulation
python drive_simulator.py --duration 600 --interval 1.0 --mode fleet
```

**How It Works:**
- **Separate WebSocket Endpoints**: Personal dashboard connects to `/ws/personal`, fleet to `/ws/fleet`
- **Independent Data Streams**: Each simulator broadcasts to its respective endpoint
- **No Interference**: Both dashboards receive real-time data simultaneously
- **Concurrent Sessions**: Each simulator runs independently with its own session ID
- **Automatic Routing**: Backend automatically routes data based on `simulation_mode` field

**Features:**
- ✅ Open both dashboards in different browser tabs - both stay live simultaneously
- ✅ Each simulator runs independently with its own session ID
- ✅ Retry mechanism handles temporary network issues or backend overload
- ✅ Both modes can post data at 1-second intervals without timing out
- ✅ Separate session tracking ensures scores don't interfere with each other
- ✅ Backend handles concurrent requests using semaphore-based rate limiting (up to 10 concurrent requests)
- ✅ WebSocket connections are completely isolated - no data crosstalk

### Simulator Options

```bash
python drive_simulator.py [OPTIONS]

Options:
  --duration SECONDS    Simulation duration (default: 300)
  --interval SECONDS    Data update interval in seconds (default: 1.0, supports as low as 1.0s)
  --mode MODE          Simulation mode: personal or fleet (default: personal)
  --api-url URL        Backend API URL (default: http://localhost:8000/api)
```

**Retry Behavior:**
- Automatic retry on timeout or connection errors
- Exponential backoff: 0.5s, 1.0s, 2.0s between retries
- Maximum 3 retry attempts per request
- Clear console feedback on retry attempts

**Session Statistics:**
Each simulation displays:
- Current score for each update
- Running average score across the session
- Session summary at completion (total updates, avg/best/worst scores)

**📚 For detailed simulation guide, troubleshooting, and advanced usage, see [SIMULATION_GUIDE.md](SIMULATION_GUIDE.md)**

---

## 🔧 Troubleshooting

### Timeout Issues

If you experience timeout errors:

1. **Check Backend Status**: Ensure the backend is running and healthy at `http://localhost:8000/health`

2. **Reduce Update Interval**: Try increasing `--interval` to 2.0 or 3.0 seconds:
   ```bash
   python drive_simulator.py --interval 2.0
   ```

3. **Monitor Backend Logs**: Check for error messages in the backend terminal

4. **Verify Concurrency Limit**: With many simulators, adjust `MAX_CONCURRENT_REQUESTS` in `backend/main.py`

5. **Test Retry Mechanism**: The simulator will show retry attempts in console:
   ```
   ⏳ Request timeout, retrying in 1.0s (attempt 2/3)...
   ```

### Backend Overload

If backend returns partial responses (confidence < 0.95):
- Backend is temporarily overloaded
- Simulator receives default score (5.0) to maintain operation
- Consider reducing number of concurrent simulators
- Or increase `MAX_CONCURRENT_REQUESTS` value

---

### Performance Optimizations

- **Async Endpoints**: All data endpoints are asynchronous for high throughput
- **Non-Blocking WebSocket**: WebSocket connections don't block HTTP requests
- **Error Recovery**: Automatic fallback to rule-based scoring if ML model fails
- **Retry Mechanism**: Simulator automatically retries failed requests with exponential backoff (0.5s, 1.0s, 2.0s)
- **Timeout Handling**: 10-second timeout for API requests with graceful degradation
- **Concurrent Support**: Semaphore-based concurrency control handles up to 10 simultaneous requests
- **Partial Responses**: Backend returns partial responses (score 5.0, confidence 0.5) when overloaded
- **Session Tracking**: Each simulator run gets unique session ID for independent tracking
- **Background Tasks**: WebSocket broadcasting and database storage run asynchronously

---

## 📁 Project Structure

```
Auralis.ai/
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.jsx         # Personal dashboard
│   │   │   ├── FleetDashboard.jsx    # Fleet dashboard (NEW)
│   │   │   ├── DriverCard.jsx        # Driver card (NEW)
│   │   │   ├── DriverRankings.jsx    # Rankings (NEW)
│   │   │   ├── FleetStats.jsx        # Fleet stats (NEW)
│   │   │   ├── FleetInsights.jsx     # AI insights (NEW)
│   │   │   ├── Header.jsx
│   │   │   ├── ScoreDisplay.jsx
│   │   │   ├── TelemetryCharts.jsx
│   │   │   ├── FeedbackPanel.jsx
│   │   │   └── StatsCards.jsx
│   │   ├── hooks/            # Custom React hooks
│   │   │   ├── useDarkMode.js
│   │   │   └── useWebSocket.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                   # FastAPI backend
│   ├── app/
│   │   └── routes.py         # API endpoints
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   ├── services/
│   │   ├── ml_service.py     # ML inference service
│   │   └── supabase_service.py # Database service
│   ├── main.py               # FastAPI application
│   ├── requirements.txt
│   └── .env.example
│
├── ml_model/                  # Machine Learning
│   ├── generate_data.py      # Synthetic data generation
│   ├── train_model.py        # Model training script
│   ├── requirements.txt
│   └── trained_model.pkl     # Trained model (generated)
│
├── simulation/                # Driving simulator
│   ├── drive_simulator.py    # Main simulator
│   └── requirements.txt
│
├── scripts/                   # Utility scripts
│   └── generate_fleet_data.py # Fleet data generator (NEW)
│
├── docs/                      # Documentation
│   ├── database_schema.md       # Base Supabase schema
│   ├── fleet_database_schema.md # Fleet tables (NEW)
│   └── FLEET_DASHBOARD.md       # Fleet guide (NEW)
│
└── README.md
```

---

## ⚙️ Configuration

### Backend Configuration (.env)

```env
# Supabase (Optional - for data persistence)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Ollama (Optional - for AI feedback)
OLLAMA_API_URL=http://localhost:11434

# Model
MODEL_PATH=../ml_model/trained_model.pkl

# Server
HOST=0.0.0.0
PORT=8000
```

### Supabase Setup

### Supabase Setup

1. Create account at [supabase.com](https://supabase.com)
2. Create a new project
3. Run the SQL schema from `docs/database_schema.md` (required for all features)
4. For fleet dashboard, also run `docs/fleet_database_schema.md` (adds drivers, vehicles, stats tables)
5. Copy your project URL and anon key to `.env`

### Ollama Setup (Optional - for AI Feedback)

For AI-powered feedback using Mistral 7B:

```bash
# Install Ollama
# Visit https://ollama.ai

# Pull the Mistral model (recommended for fleet dashboard)
ollama pull mistral

# Alternatively, use llama2
ollama pull llama2

# Run Ollama service
ollama serve
```

The system will automatically use the configured model for:
- Personal dashboard feedback
- Per-driver performance analysis (fleet)
- Fleet-level insights and recommendations

---

## 🔧 Backend Improvements

### Enhanced Error Handling

The backend now includes robust error handling for common issues:

1. **ML Model Loading**
   - Graceful fallback to rule-based scoring if model file is missing
   - Handles pickle import errors (e.g., missing classes)
   - Clear console messages indicating which scoring method is active

2. **Score Calculation**
   - Try/except wrapper around all score calculations
   - Returns fallback score (5.0) if calculation fails
   - Never crashes due to NoneType errors

3. **Persistent Scoring Object**
   - ML service initialized at startup (during lifespan)
   - Prevents 'NoneType' errors in calculate_score
   - Available throughout application lifetime via `app.state.ml_service`

4. **Async Optimization**
   - All data endpoints use `async def` for better concurrency
   - WebSocket endpoint doesn't block HTTP requests
   - Handles multiple simulator connections at 1-second intervals
   - Broadcasting to WebSocket clients runs in background tasks

### WebSocket Enhancements

- **Parallel Streaming**: Separate endpoints (`/ws/personal` and `/ws/fleet`) for independent data streams
- **Dedicated Connection Pools**: Personal and fleet connections are managed separately
- **Concurrent Client Support**: Handle multiple dashboards simultaneously
- **Automatic Routing**: Broadcasts are routed based on `mode` field to correct endpoint
- **Backward Compatibility**: Legacy `/ws` endpoint still works (routes to personal)
- **Automatic Cleanup**: Disconnected clients are automatically removed
- **Error Resilience**: Failed broadcasts don't crash the connection manager

### API Response Format

All `/api/driving_data` responses now include:
```json
{
  "score": 8.5,
  "timestamp": "2025-10-17T20:30:00.000000",
  "confidence": 0.95
}
```

WebSocket broadcasts are routed to appropriate endpoints:
- Personal mode data (`mode: "personal"`) → `/ws/personal`
- Fleet mode data (`mode: "fleet"`) → `/ws/fleet`

```json
{
  "type": "driving_data",
  "mode": "personal",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "payload": {
    "speed": 60.5,
    "acceleration": 0.5,
    "scenario": "normal",
    "score": 8.5
  }
}
```

**WebSocket Endpoints:**
- `/ws/personal` - For personal dashboard (individual driver)
- `/ws/fleet` - For fleet dashboard (multiple drivers/vehicles)
- `/ws` - Legacy endpoint (backward compatibility, routes to personal)

Partial response when backend is overloaded:
```json
{
  "score": 5.0,
  "timestamp": "2025-10-17T20:30:00.000000",
  "confidence": 0.5
}
```
(Lower confidence value indicates a partial/default response)

---

## 🛠️ Development

### Running Tests

```bash
# Backend tests (if implemented)
cd backend
pytest

# Frontend tests (if implemented)
cd frontend
npm test
```

### Linting

```bash
# Frontend
cd frontend
npm run lint

# Backend (using flake8 or black)
cd backend
flake8 .
black .
```

### Building for Production

```bash
# Frontend
cd frontend
npm run build

# Backend (already production-ready with uvicorn)
```

---

## 🚢 Deployment

### Local macOS (Current Setup)
Everything runs locally - perfect for development and testing.

### Future Raspberry Pi Deployment
The project structure supports deployment to Raspberry Pi:
1. Install Python 3.13+ on Pi
2. Clone repository
3. Follow installation steps
4. Configure to start on boot

### Cloud Deployment
- **Frontend**: Deploy to Vercel, Netlify, or any static host
- **Backend**: Deploy to Railway, Render, or any Python-compatible platform
- **Database**: Already using Supabase (cloud-based)

---

## 🚗 Fleet Dashboard

The Fleet Dashboard is perfect for fleet operators (Uber, Ola, delivery services, etc.) who need to:
- Monitor multiple drivers simultaneously
- Track driver performance and safety
- Identify training needs
- Get AI-powered insights

### Key Features
- **Multi-Driver Tracking**: Monitor entire fleet at once
- **Driver Rankings**: See top performers and those needing support
- **AI Feedback**: Mistral 7B generates personalized driver insights
- **Fleet Analytics**: Understand fleet-wide trends and patterns
- **Scalable**: Easily add more drivers and vehicles

### Quick Start

1. **Setup Database**: Run SQL from `docs/fleet_database_schema.md`
2. **Generate Sample Data**: 
   ```bash
   python scripts/generate_fleet_data.py --drivers 5 --sessions 10
   ```
3. **Access Dashboard**: Navigate to `http://localhost:3000/dashboard/fleet`

### Documentation
Complete guide available at [docs/FLEET_DASHBOARD.md](docs/FLEET_DASHBOARD.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ for safer driving
- Powered by React, FastAPI, TensorFlow, and Supabase
- Inspired by the need for better driver training and awareness

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the maintainers

---

**Drive Safe! 🚗💨**
