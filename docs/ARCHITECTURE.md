# DriveMind.ai - Technical Architecture

## System Overview

DriveMind.ai is a full-stack AI-powered driver safety scoring system with the following components:

```
┌─────────────────────────────────────────────────────────────────┐
│                        DriveMind.ai System                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│   Frontend   │◄──────►│   Backend    │◄──────►│   Database   │
│   (React)    │  HTTP/ │   (FastAPI)  │  API   │  (Supabase)  │
│              │  WS    │              │        │              │
└──────────────┘        └──────────────┘        └──────────────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
            ┌───────▼────┐  ┌──▼────┐  ┌─▼──────┐
            │ ML Service │  │ Ollama │  │ Simulator│
            │  (Score)   │  │  LLM   │  │  (Test) │
            └────────────┘  └────────┘  └─────────┘
```

## Technology Stack

### Frontend
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Styling**: TailwindCSS 3.3
- **Charts**: Recharts 2.10
- **Animations**: Framer Motion 10.16
- **Icons**: Lucide React 0.292
- **State Management**: React Hooks (useState, useEffect)
- **WebSocket**: Native WebSocket API

### Backend
- **Framework**: FastAPI 0.109
- **Web Server**: Uvicorn 0.27
- **Real-time**: WebSockets 12.0
- **Validation**: Pydantic 2.5
- **Database Client**: Supabase 2.3
- **Environment**: Python-dotenv 1.0
- **HTTP Client**: Requests 2.31

### Machine Learning
- **Core**: NumPy 1.26, Pandas 2.1
- **ML Frameworks**: 
  - scikit-learn 1.4 (Random Forest, Gradient Boosting)
  - TensorFlow 2.16 (Neural Networks)
  - TensorFlow-Metal (macOS GPU acceleration)
- **Model Persistence**: Joblib 1.3, Pickle
- **Visualization**: Matplotlib 3.8

### Database
- **Platform**: Supabase (PostgreSQL)
- **Tables**: sessions, events, scores, feedback
- **Features**: Row Level Security, Real-time subscriptions

### Optional Components
- **LLM**: Ollama (llama2, mistral, etc.)
- **Purpose**: AI-generated driving feedback

## Architecture Details

### Frontend Architecture

```
src/
├── components/
│   ├── Dashboard.jsx          # Main dashboard container
│   ├── Header.jsx             # App header with dark mode
│   ├── ScoreDisplay.jsx       # Circular score gauge
│   ├── TelemetryCharts.jsx    # Real-time line charts
│   ├── FeedbackPanel.jsx      # AI feedback display
│   └── StatsCards.jsx         # Metric cards
├── hooks/
│   ├── useDarkMode.js         # Dark mode state management
│   └── useWebSocket.js        # WebSocket connection
├── App.jsx                    # Root component
└── main.jsx                   # Application entry
```

**Key Features**:
- Real-time data updates via WebSocket
- Responsive design (mobile, tablet, desktop)
- Dark mode with localStorage persistence
- Smooth animations and transitions
- Optimized chart rendering

### Backend Architecture

```
backend/
├── app/
│   └── routes.py              # API endpoints
├── models/
│   └── schemas.py             # Pydantic models
├── services/
│   ├── ml_service.py          # ML inference
│   └── supabase_service.py    # Database operations
└── main.py                    # FastAPI app
```

**API Endpoints**:
- `POST /api/driving_data` - Receive telemetry and calculate score
- `GET /api/current_score` - Get latest score
- `POST /api/feedback` - Generate AI feedback
- `POST /api/session` - Create driving session
- `GET /api/sessions/{id}` - Get session history
- `GET /health` - Health check
- `WS /ws` - WebSocket connection

### ML Model Pipeline

```
generate_data.py → training_data.csv → train_model.py → trained_model.pkl
                                                       ↓
                                              ml_service.py (inference)
```

**Training Process**:
1. Generate synthetic data with realistic driving profiles
2. Extract features: speed, acceleration, braking, steering, jerk
3. Train multiple models (RF, GB, NN) and select best
4. Export model for inference

**Inference Process**:
1. Receive driving telemetry
2. Extract features from data
3. Run model prediction
4. Apply rule-based fallback if model unavailable
5. Return score (0-10)

### Data Flow

```
Simulator → Backend API → ML Model → Score
    ↓                                  ↓
WebSocket ←─────────────────────── Frontend
    ↓                                  ↓
Database ←─────────────────────── Display
```

**Real-time Flow**:
1. Simulator sends telemetry every 1 second
2. Backend calculates score using ML model
3. Backend broadcasts to all WebSocket clients
4. Frontend updates charts and score display
5. Backend optionally stores in Supabase

## Scalability Considerations

### Current Architecture (Single Instance)
- Handles: ~100 concurrent users
- WebSocket connections: Up to 1000
- Database: Supabase (auto-scaling)
- ML inference: CPU-based, ~10ms latency

### Future Scaling Options

**Horizontal Scaling**:
- Load balancer (nginx, HAProxy)
- Multiple backend instances
- Redis for WebSocket pub/sub
- Kubernetes deployment

**Performance Optimization**:
- Model caching (Redis)
- Database connection pooling
- CDN for frontend assets
- Batch processing for analytics

**ML Optimization**:
- GPU acceleration (CUDA, Metal)
- Model quantization (TFLite)
- Edge deployment (Raspberry Pi)
- Online learning for model updates

## Security

### Current Implementation
- CORS configured for localhost
- Environment variables for secrets
- Input validation with Pydantic
- Optional RLS on Supabase

### Production Recommendations
- HTTPS/WSS encryption
- Authentication (JWT, OAuth)
- Rate limiting
- API key management
- Database RLS policies
- Input sanitization
- Security headers

## Deployment Options

### Local Development (Current)
```bash
# Terminal 1: Backend
uvicorn main:app --reload

# Terminal 2: Frontend
npm run dev

# Terminal 3: Simulator
python drive_simulator.py
```

### Production Deployment

**Frontend**:
- Vercel, Netlify, or Cloudflare Pages
- Static build with `npm run build`
- Environment variables for API URL

**Backend**:
- Railway, Render, or AWS EC2
- Docker container
- PM2 for process management
- Environment variables for secrets

**Database**:
- Supabase (managed PostgreSQL)
- Automated backups
- Connection pooling

**ML Model**:
- Package with backend
- Optional: Separate ML inference service
- Model versioning with MLflow

### Raspberry Pi Deployment
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3-pip nodejs npm

# Clone and setup
git clone <repo>
./scripts/setup.sh

# Configure systemd services
# - backend.service
# - frontend.service
# - simulator.service (optional)

# Enable on boot
sudo systemctl enable backend
sudo systemctl enable frontend
```

## Monitoring and Observability

### Recommended Tools
- **Application**: Sentry (error tracking)
- **Metrics**: Prometheus + Grafana
- **Logs**: ELK stack or Loki
- **Uptime**: UptimeRobot, Pingdom
- **Database**: Supabase dashboard

### Key Metrics
- WebSocket connection count
- API response time
- ML inference latency
- Error rate
- Database query performance
- Frontend page load time

## Future Enhancements

### Planned Features
1. Multi-user support with authentication
2. Historical analytics dashboard
3. Driver comparison and rankings
4. Mobile app (React Native)
5. Real vehicle sensor integration
6. Advanced ML models (LSTM, Transformer)
7. Predictive collision detection
8. Voice feedback with TTS
9. Export reports (PDF, CSV)
10. Integration with fleet management systems

### Research Areas
- Federated learning for privacy
- Explainable AI for scoring decisions
- Computer vision for distraction detection
- Edge computing for real-time processing
- Multi-modal sensor fusion
