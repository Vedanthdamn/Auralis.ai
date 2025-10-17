# Development Guide

This guide covers development workflows, best practices, and troubleshooting for DriveMind.ai.

## Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Git
- (Optional) Ollama for AI feedback
- (Optional) Supabase account

### Initial Setup

```bash
# Clone repository
git clone https://github.com/Vedanthdamn/Auralis.ai.git
cd Auralis.ai

# Run automated setup
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Setup

If automated setup fails, follow these steps:

#### 1. Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Test that it works
```

#### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

#### 3. ML Model Setup
```bash
cd ml_model
pip install -r requirements.txt
python generate_data.py
python train_model.py
```

#### 4. Simulation Setup
```bash
cd simulation
pip install -r requirements.txt
```

## Development Workflow

### Running the Development Environment

**Option 1: Three Terminal Windows**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Terminal 3 - Simulator:
```bash
cd simulation
python drive_simulator.py --duration 300 --interval 1.0
```

**Option 2: Using tmux/screen (Linux/macOS)**
```bash
# Create tmux session
tmux new -s drivemind

# Split into panes (Ctrl+B then %)
# Run each component in separate pane
```

### Making Changes

#### Frontend Changes
1. Edit files in `frontend/src/`
2. Changes hot-reload automatically
3. Check browser console for errors
4. Test on different screen sizes

#### Backend Changes
1. Edit files in `backend/`
2. FastAPI auto-reloads with `--reload` flag
3. Check terminal for errors
4. Test endpoints with curl or Postman

#### ML Model Changes
1. Edit `ml_model/generate_data.py` or `train_model.py`
2. Re-run training: `python train_model.py`
3. Restart backend to load new model
4. Verify scoring changes

## Testing

### Frontend Testing

**Manual Testing**:
```bash
cd frontend
npm run dev
```
- Open http://localhost:3000
- Test dark mode toggle
- Verify charts update
- Check responsive design
- Test WebSocket connection

**Linting**:
```bash
npm run lint
```

**Build Test**:
```bash
npm run build
npm run preview
```

### Backend Testing

**Manual Testing**:
```bash
# Health check
curl http://localhost:8000/health

# Send driving data
curl -X POST http://localhost:8000/api/driving_data \
  -H "Content-Type: application/json" \
  -d '{
    "speed": 60.5,
    "acceleration": 0.5,
    "braking_intensity": 0.0,
    "steering_angle": 5.2,
    "jerk": 0.1,
    "timestamp": "2024-01-01T12:00:00"
  }'

# Get current score
curl http://localhost:8000/api/current_score
```

**API Documentation**:
- Open http://localhost:8000/docs (Swagger UI)
- Open http://localhost:8000/redoc (ReDoc)

### ML Model Testing

```bash
cd ml_model

# Test data generation
python generate_data.py

# Test model training
python train_model.py

# Verify model file exists
ls -lh trained_model.pkl
```

### Simulation Testing

```bash
cd simulation

# Short test run
python drive_simulator.py --duration 30 --interval 1.0

# Verify API communication
# Check backend logs for received data
```

## Code Style

### Frontend (JavaScript/React)
- Use functional components
- Follow React Hooks best practices
- Use meaningful variable names
- Add PropTypes or TypeScript for type safety
- Keep components small and focused
- Use TailwindCSS utility classes

Example:
```jsx
function MyComponent({ data, onUpdate }) {
  const [state, setState] = useState(null)
  
  useEffect(() => {
    // Side effects
  }, [data])
  
  return (
    <div className="card">
      {/* JSX */}
    </div>
  )
}
```

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints
- Add docstrings to functions
- Keep functions small and focused
- Use async/await for I/O operations

Example:
```python
async def process_data(data: DrivingData) -> float:
    """
    Process driving data and return score.
    
    Args:
        data: DrivingData object
        
    Returns:
        float: Safety score (0-10)
    """
    # Implementation
    return score
```

## Debugging

### Frontend Debugging

**Chrome DevTools**:
1. Open DevTools (F12)
2. Check Console for errors
3. Use Network tab for API calls
4. Use React DevTools extension

**Common Issues**:
- WebSocket not connecting: Check backend is running
- Charts not updating: Check console for data format
- Dark mode not persisting: Check localStorage

### Backend Debugging

**Print Debugging**:
```python
print(f"Received data: {data}")
print(f"Calculated score: {score}")
```

**FastAPI Debug Mode**:
```python
# In main.py
app = FastAPI(debug=True)
```

**Common Issues**:
- Import errors: Check virtual environment is activated
- Model not loading: Check file path in .env
- CORS errors: Check allowed origins in main.py

### ML Model Debugging

**Check Model Output**:
```python
import pickle

with open('trained_model.pkl', 'rb') as f:
    model_data = pickle.load(f)
    
model = model_data['model']
test_features = [[60, 0.5, 0.1, 5, 0.1]]
prediction = model.predict(test_features)
print(f"Score: {prediction[0]}")
```

## Common Issues and Solutions

### Issue: Frontend won't build
**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Issue: Backend won't start
**Solution**:
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Model training fails
**Solution**:
```bash
# Check data file exists
ls -lh training_data.csv

# Regenerate data
python generate_data.py

# Install missing dependencies
pip install numpy pandas scikit-learn
```

### Issue: WebSocket disconnects frequently
**Solution**:
- Check network stability
- Increase reconnect timeout in frontend
- Check backend logs for errors
- Verify firewall settings

### Issue: Slow performance
**Solution**:
- Reduce chart update frequency
- Limit data points in charts (currently 30)
- Optimize ML model (use simpler model)
- Enable production builds

## Performance Optimization

### Frontend
- Use React.memo for expensive components
- Debounce frequent updates
- Lazy load components
- Optimize bundle size with code splitting

### Backend
- Use async endpoints for I/O
- Cache ML model predictions
- Batch database writes
- Use connection pooling

### ML Model
- Use simpler models (Random Forest vs Neural Network)
- Reduce model size
- Use model quantization
- Cache predictions

## Contributing

### Branching Strategy
- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes

### Commit Messages
```
feat: Add new telemetry chart
fix: Resolve WebSocket reconnection issue
docs: Update setup instructions
refactor: Simplify scoring algorithm
test: Add unit tests for ML service
```

### Pull Request Process
1. Create feature branch
2. Make changes
3. Test thoroughly
4. Update documentation
5. Submit PR with description
6. Address review comments

## Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database migrations prepared
- [ ] Security audit completed

### Deployment Steps
1. Build frontend: `npm run build`
2. Test production build locally
3. Deploy frontend to hosting
4. Deploy backend to server
5. Run database migrations
6. Update environment variables
7. Test live system
8. Monitor for errors

### Post-deployment
- [ ] Verify frontend loads
- [ ] Test API endpoints
- [ ] Check WebSocket connections
- [ ] Monitor error logs
- [ ] Check database connections
- [ ] Verify SSL/TLS certificates

## Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- TailwindCSS: https://tailwindcss.com/
- Recharts: https://recharts.org/
- scikit-learn: https://scikit-learn.org/

### Tools
- Postman: API testing
- React DevTools: Component debugging
- Chrome DevTools: Frontend debugging
- pgAdmin: Database management
- Sentry: Error tracking

### Community
- GitHub Issues: Bug reports and features
- Stack Overflow: Technical questions
- Discord/Slack: Real-time chat (if available)

## Troubleshooting Contact

For issues not covered in this guide:
1. Check existing GitHub issues
2. Search documentation
3. Create new issue with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Screenshots if applicable
