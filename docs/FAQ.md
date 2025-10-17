# Frequently Asked Questions (FAQ)

## General Questions

### What is DriveMind.ai?
DriveMind.ai is an AI-powered driver safety scoring system that analyzes driving behavior in real-time and provides safety scores and feedback to help improve driving habits.

### Is this for real cars or simulation?
Currently, the system uses simulated driving data for testing and development. However, the architecture is designed to support real vehicle sensor data integration in the future.

### What platforms are supported?
- **macOS** (primary development platform with Apple Silicon optimization)
- **Linux** (tested on Ubuntu)
- **Windows** (should work but less tested)
- **Raspberry Pi** (future deployment target)

### Do I need special hardware?
No special hardware is required. The system runs on standard computers. For production deployment with real vehicles, you would need appropriate sensors (OBD-II adapter, GPS, accelerometer, etc.).

## Setup and Installation

### Q: Setup script fails, what should I do?
**A:** Try manual setup:
1. Install Node.js dependencies: `cd frontend && npm install`
2. Create Python venv: `cd backend && python3 -m venv venv`
3. Install Python packages: `source venv/bin/activate && pip install -r requirements.txt`
4. Train model: `cd ml_model && python train_model.py`

### Q: Can I run this without Supabase?
**A:** Yes! Supabase is optional. The system works perfectly fine without it. You'll just miss data persistence features. Update `backend/.env` to skip Supabase configuration.

### Q: Can I run this without Ollama?
**A:** Yes! Ollama is optional for AI-generated feedback. Without it, the system uses rule-based feedback which works well. Simply skip the Ollama installation.

### Q: What Python version do I need?
**A:** Python 3.9 or higher is required. Check with `python3 --version`.

### Q: npm install fails with errors, what do I do?
**A:** Try:
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

## Usage Questions

### Q: How do I start the system?
**A:** You need three terminal windows:
1. Backend: `cd backend && source venv/bin/activate && uvicorn main:app --reload`
2. Frontend: `cd frontend && npm run dev`
3. Simulator: `cd simulation && python drive_simulator.py`

Then open http://localhost:3000 in your browser.

### Q: The dashboard shows "Disconnected", what's wrong?
**A:** This means the WebSocket connection to the backend failed. Check:
1. Backend is running on port 8000
2. No firewall blocking connections
3. Check browser console for errors

### Q: Charts aren't updating, why?
**A:** Verify:
1. Simulator is running and sending data
2. Backend is receiving data (check terminal logs)
3. WebSocket connection is established (green indicator)
4. No JavaScript errors in browser console

### Q: Scores seem wrong or random, why?
**A:** Possible causes:
1. Model not trained yet - run `cd ml_model && python train_model.py`
2. Model file not found - check `backend/.env` MODEL_PATH
3. Using rule-based fallback - this is expected if model unavailable

### Q: How do I change the simulation parameters?
**A:** Run simulator with custom parameters:
```bash
python drive_simulator.py --duration 600 --interval 0.5 --api-url http://localhost:8000/api
```

### Q: Can I test the API without the frontend?
**A:** Yes! Use curl or Postman:
```bash
curl -X POST http://localhost:8000/api/driving_data \
  -H "Content-Type: application/json" \
  -d '{"speed": 60, "acceleration": 0.5, "braking_intensity": 0.0, "steering_angle": 5, "jerk": 0.1, "timestamp": "2024-01-01T12:00:00"}'
```

## Machine Learning Questions

### Q: How accurate is the ML model?
**A:** On synthetic test data, the model achieves R² scores of 0.85-0.95 depending on which algorithm is used. Real-world accuracy depends on training data quality.

### Q: Can I train on custom data?
**A:** Yes! Replace the data in `training_data.csv` with your own data in the same format, then run `python train_model.py`.

### Q: Which ML model is best?
**A:** The training script automatically selects the best model. Usually:
- Random Forest: Fast, good for real-time
- Gradient Boosting: Best accuracy
- Neural Network: Best for complex patterns (needs more data)

### Q: How do I retrain the model?
**A:**
```bash
cd ml_model
python generate_data.py  # Generate fresh data
python train_model.py    # Train new model
# Restart backend to load new model
```

### Q: Does it work on Apple Silicon (M1/M2/M4)?
**A:** Yes! TensorFlow is configured to use Metal acceleration on macOS. This provides significant speedup for neural network training.

### Q: Training fails with memory errors, what to do?
**A:** Reduce the number of samples in `generate_data.py`:
```python
X, y = generate_driving_data(n_samples=5000)  # Instead of 10000
```

## Database Questions

### Q: Do I need a database to use the system?
**A:** No! The database (Supabase) is optional. The system works perfectly fine without it for real-time monitoring.

### Q: How do I set up Supabase?
**A:**
1. Create account at https://supabase.com
2. Create new project
3. Go to SQL editor
4. Run SQL from `docs/database_schema.md`
5. Copy URL and anon key to `backend/.env`

### Q: Can I use PostgreSQL instead of Supabase?
**A:** Yes, but you'll need to modify `backend/services/supabase_service.py` to use direct PostgreSQL connection instead of Supabase client.

### Q: How do I view stored data?
**A:** Use Supabase dashboard:
1. Go to your project
2. Click "Table Editor"
3. View sessions, events, scores, feedback tables

## Frontend Questions

### Q: How do I enable dark mode?
**A:** Click the moon/sun icon in the top-right corner. Your preference is saved in browser localStorage.

### Q: Can I customize the UI?
**A:** Yes! Edit files in `frontend/src/components/`. The project uses TailwindCSS for styling.

### Q: How do I change colors?
**A:** Edit `frontend/tailwind.config.js` and modify the color palette in the `theme.extend.colors` section.

### Q: Charts are laggy, how to fix?
**A:** Reduce the number of data points displayed:
```javascript
// In TelemetryCharts.jsx
const maxDataPoints = 20  // Instead of 30
```

### Q: Can I add more charts?
**A:** Yes! Create new chart components in `frontend/src/components/` using Recharts library.

## Deployment Questions

### Q: How do I deploy to production?
**A:**
1. Frontend: Build with `npm run build`, deploy to Vercel/Netlify
2. Backend: Deploy to Railway/Render with Dockerfile
3. Update environment variables on each platform

### Q: Can I deploy to Raspberry Pi?
**A:** Yes! The project is designed for Pi deployment. Follow these steps:
```bash
# On Raspberry Pi
git clone <repo>
./scripts/setup.sh
# Configure systemd services to run on boot
```

### Q: What about HTTPS/SSL?
**A:** For production:
- Frontend: Automatic with Vercel/Netlify
- Backend: Use nginx reverse proxy with Let's Encrypt
- WebSocket: Change to WSS protocol

### Q: How do I handle multiple users?
**A:** Currently designed for single user. For multi-user:
1. Add authentication (JWT)
2. Add user management
3. Separate sessions per user
4. Use Redis for session management

## Performance Questions

### Q: How many concurrent users can it handle?
**A:** Current single-instance setup: ~100 concurrent WebSocket connections. For more, use horizontal scaling with load balancer and Redis.

### Q: How fast is the scoring?
**A:** ML inference takes ~10ms on modern CPU. Total API response time is typically under 50ms.

### Q: Can I optimize for faster response?
**A:** Yes:
1. Use simpler ML model (Random Forest)
2. Cache recent predictions
3. Reduce data validation
4. Use production ASGI server (gunicorn)

### Q: System uses too much memory, why?
**A:** Likely causes:
1. TensorFlow loading large model
2. Many historical chart data points
3. Multiple browser tabs open
Solution: Use smaller models, limit data retention

## Troubleshooting

### Q: Error: "Module not found"
**A:** Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Q: Error: "CORS policy blocked"
**A:** Check CORS settings in `backend/main.py`. Ensure frontend URL is in allowed origins.

### Q: Error: "WebSocket connection failed"
**A:** Verify:
1. Backend running on correct port (8000)
2. No proxy/firewall blocking WebSocket
3. Correct WebSocket URL in frontend

### Q: Error: "Model file not found"
**A:** Train the model first:
```bash
cd ml_model
python train_model.py
```

### Q: Frontend shows blank page
**A:** Check browser console for errors. Common fixes:
1. Clear browser cache
2. Rebuild frontend: `npm run build`
3. Check for JavaScript errors

## Integration Questions

### Q: Can I integrate with my existing system?
**A:** Yes! The API is RESTful and well-documented. See `docs/api_example.py` for integration examples.

### Q: Can I use a different frontend framework?
**A:** Yes! The backend is framework-agnostic. You can build a Vue, Angular, or mobile app that consumes the API.

### Q: Can I add more sensors?
**A:** Yes! Modify `models/schemas.py` to add new fields, update ML model to include new features.

### Q: How do I export data?
**A:** Query Supabase database or add export endpoint to backend:
```python
@router.get("/export/{session_id}")
async def export_session(session_id: str):
    # Return CSV or JSON
```

## Advanced Questions

### Q: How do I add custom scoring algorithms?
**A:** Edit `backend/services/ml_service.py` and modify the `_rule_based_score()` method or add new model types.

### Q: Can I use different LLMs for feedback?
**A:** Yes! Modify `ml_service.py` to use OpenAI, Anthropic, or other LLM APIs instead of Ollama.

### Q: How do I implement user authentication?
**A:** Add FastAPI dependency:
```python
from fastapi.security import OAuth2PasswordBearer
# Implement JWT authentication
```

### Q: Can I add video processing?
**A:** Yes, but requires significant additional work:
1. Add video upload endpoint
2. Implement computer vision (OpenCV, YOLO)
3. Process frames for distraction detection
4. Integrate results into scoring

## Still Need Help?

- Check the documentation in `docs/`
- Search existing GitHub issues
- Create new issue with detailed description
- Join community discussions (if available)
