# DriveMind.ai 🚗

**AI-Powered Driver Safety Scoring System**

Illuminating Safer Journeys with AI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-61dafb.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)

---

> **🔧 Python 3.13 Installation Fixed!**
> 
> We've resolved the dependency conflicts. Installation now works smoothly on Python 3.12 and 3.13!
> 
> **Quick Start:** [PYTHON_313_QUICK_START.md](PYTHON_313_QUICK_START.md)
> 
> **Full Guide:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

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

### Frontend (React + Vite)
- 📊 Real-time charts for speed, acceleration, and braking
- 🎯 Live driving score display with animated gauge
- 🤖 AI-generated feedback panel
- 🌓 Dark mode toggle with persistent preferences
- 📱 Fully responsive design
- ✨ Smooth animations with Framer Motion
- 🎨 Beautiful UI with TailwindCSS

### Backend (FastAPI)
- 🚀 High-performance async API
- 🔌 WebSocket support for real-time data streaming
- 🧠 ML inference for safety scoring
- 🤖 Optional Ollama LLM integration for feedback
- 💾 Supabase database integration
- 📝 Comprehensive API documentation
- ✅ Request validation with Pydantic

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

---

## 🏗️ Architecture

```
┌─────────────────┐     WebSocket      ┌──────────────────┐
│  React Frontend │◄──────────────────►│  FastAPI Backend │
│  (Port 3000)    │                    │   (Port 8000)    │
└─────────────────┘                    └──────────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────┐
                    │                         │                     │
            ┌───────▼──────┐         ┌────────▼────────┐   ┌───────▼──────┐
            │  ML Service  │         │ Supabase Service│   │Ollama (opt.) │
            │  (Scoring)   │         │   (Database)    │   │   (LLM)      │
            └──────────────┘         └─────────────────┘   └──────────────┘
                    ▲
                    │
            ┌───────┴──────┐
            │  Simulator   │
            │ (Test Data)  │
            └──────────────┘
```

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

#### Terminal 3: Run Simulation
```bash
cd simulation
python drive_simulator.py --duration 300 --interval 1.0
```

### Access the Dashboard

Open your browser and navigate to:
```
http://localhost:3000
```

You should see:
- Real-time telemetry charts updating
- Live driving score
- AI-generated feedback (if Ollama is configured)

---

## 📁 Project Structure

```
Auralis.ai/
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.jsx
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
├── docs/                      # Documentation
│   └── database_schema.md    # Supabase schema
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

1. Create account at [supabase.com](https://supabase.com)
2. Create a new project
3. Run the SQL schema from `docs/database_schema.md`
4. Copy your project URL and anon key to `.env`

### Ollama Setup (Optional)

```bash
# Install Ollama
# Visit https://ollama.ai

# Pull a model
ollama pull llama2

# Run Ollama service
ollama serve
```

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
