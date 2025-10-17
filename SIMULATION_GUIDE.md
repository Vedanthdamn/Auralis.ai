# DriveMind.ai Simulation Guide

Complete guide for running driving simulations with DriveMind.ai

## Overview

DriveMind.ai supports two independent simulation modes that can run concurrently:

- **Personal Mode** 🚗: Individual driver testing and training
- **Fleet Mode** 🚕: Fleet management and multi-vehicle monitoring

## Quick Start

### 1. Start the Backend

```bash
cd backend
source venv/bin/activate  # If using virtual environment
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Run Simulations

#### Option A: Using Convenience Scripts

```bash
cd simulation

# Personal mode (default: 300s duration, 1.0s interval)
./run_personal.sh

# Fleet mode (default: 300s duration, 1.0s interval)
./run_fleet.sh

# Custom duration and interval
./run_personal.sh 600 0.5  # 600 seconds, 0.5s interval
./run_fleet.sh 180 2.0     # 180 seconds, 2.0s interval
```

#### Option B: Using Python Directly

```bash
cd simulation

# Personal mode
python drive_simulator.py --duration 300 --interval 1.0 --mode personal

# Fleet mode
python drive_simulator.py --duration 300 --interval 1.0 --mode fleet
```

### 3. View Results

- **Personal Dashboard**: http://localhost:3000/dashboard
- **Fleet Dashboard**: http://localhost:3000/dashboard/fleet

## Running Multiple Simulations Concurrently

You can run both personal and fleet simulations at the same time:

### Terminal Layout

```
┌─────────────────────┬─────────────────────┐
│   Terminal 1:       │   Terminal 2:       │
│   Backend Server    │   Frontend Server   │
└─────────────────────┴─────────────────────┘
┌─────────────────────┬─────────────────────┐
│   Terminal 3:       │   Terminal 4:       │
│   Personal Sim      │   Fleet Sim         │
└─────────────────────┴─────────────────────┘
```

### Commands

```bash
# Terminal 1: Backend
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Personal Simulation
cd simulation && ./run_personal.sh 600

# Terminal 4: Fleet Simulation
cd simulation && ./run_fleet.sh 600
```

## Simulation Parameters

### Command Line Options

```bash
python drive_simulator.py [OPTIONS]

Options:
  --duration SECONDS    Simulation duration in seconds (default: 300)
  --interval SECONDS    Data update interval in seconds (default: 1.0)
  --mode MODE          Simulation mode: personal or fleet (default: personal)
  --api-url URL        Backend API URL (default: http://localhost:8000/api)
```

### Examples

```bash
# Short test run (30 seconds)
python drive_simulator.py --duration 30 --interval 1.0 --mode personal

# High-frequency updates (0.5 second interval)
python drive_simulator.py --duration 300 --interval 0.5 --mode fleet

# Long-duration fleet test (10 minutes)
python drive_simulator.py --duration 600 --interval 1.0 --mode fleet

# Custom backend URL
python drive_simulator.py --api-url http://192.168.1.100:8000/api --mode personal
```

## Driving Scenarios

The simulator automatically cycles through realistic driving scenarios:

### 1. Normal City Driving (50% probability)
- Target speed: 40-70 km/h
- Smooth acceleration/deceleration
- Gentle steering inputs
- **Safety Impact**: High scores (8-10)

### 2. Highway Driving (20% probability)
- Target speed: 80-110 km/h
- Steady speed with minimal steering
- Larger following distances
- **Safety Impact**: Medium-high scores (7-9)

### 3. Aggressive Driving (15% probability)
- Target speed: 70-100 km/h
- Hard acceleration and braking
- Sharp steering inputs
- **Safety Impact**: Lower scores (5-7)

### 4. Cautious Driving (10% probability)
- Target speed: 30-50 km/h
- Very gentle acceleration/braking
- Minimal steering changes
- **Safety Impact**: High scores (9-10)

### 5. Emergency Situations (5% probability)
- Immediate braking to stop
- Possible evasive steering
- Simulates obstacle avoidance
- **Safety Impact**: Variable (6-9)

## Understanding the Output

### Console Output Format

```
🚗 [PERSONAL] Speed:  60.5 km/h | Accel:  0.50 m/s² | Brake: 0.00 | Steer:  5.2° | Scenario: normal     | Score:  9.5/10 ✅
│   │          │                 │                  │             │               │                      │
│   │          │                 │                  │             │               │                      └─ Safety score
│   │          │                 │                  │             │               └─ Current scenario
│   │          │                 │                  │             └─ Steering angle
│   │          │                 │                  └─ Braking intensity (0-1)
│   │          │                 └─ Acceleration (m/s²)
│   │          └─ Current speed
│   └─ Simulation mode
└─ Mode icon (🚗 = personal, 🚕 = fleet)
```

### Status Indicators

- ✅ **Green check**: Request successful, score received
- ⚠️ **Warning**: No response from backend (after retries)
- ⏳ **Hourglass**: Retrying request with exponential backoff
- 📍 **Pin**: Scenario change notification

## Performance Characteristics

### Backend Optimization

- **Async Endpoints**: All endpoints use `async def` for high concurrency
- **Non-Blocking WebSocket**: WebSocket connections don't block HTTP requests
- **Error Recovery**: Automatic fallback to rule-based scoring if ML model fails
- **Timeout Handling**: 10-second timeout with graceful degradation (increased from 5s)
- **Concurrency Control**: Semaphore-based rate limiting (10 concurrent requests)
- **Partial Responses**: Returns score 5.0 with confidence 0.5 when overloaded
- **Session Tracking**: Each simulation run gets unique UUID for independent tracking

### Retry Mechanism (NEW)

The simulator now automatically retries failed requests with exponential backoff:

- **Retry Attempts**: 3 maximum retries per request
- **Backoff Strategy**: 0.5s → 1.0s → 2.0s between attempts
- **Retry Triggers**: Connection errors, timeouts, HTTP 503 (backend busy)
- **Console Feedback**: Shows retry attempts and delays

Example output:
```
⏳ Request timeout, retrying in 0.5s (attempt 1/3)...
⏳ Request timeout, retrying in 1.0s (attempt 2/3)...
❌ Request timeout after 3 attempts
```

### Session Statistics (NEW)

Each simulation run tracks its own statistics:

- **Session ID**: Unique UUID for each run
- **Running Average**: Displayed on every update
- **Session Summary**: Shows at completion

Example output:
```
🚗 [PERSONAL] Speed:  60.5 km/h | ... | Score: 8.5/10 | Avg: 8.3/10 ✅

==================================================
✅ PERSONAL Simulation complete!
Session ID: 550e8400-e29b-41d4-a716-446655440000
Total updates: 42
Average score: 8.34/10
Best score: 9.50/10
Worst score: 6.20/10
```

### Recommended Settings

#### For Testing
```bash
--duration 60 --interval 1.0
```

#### For Development
```bash
--duration 300 --interval 1.0
```

#### For Demos
```bash
--duration 600 --interval 1.0
```

#### For High-Load Testing
```bash
--duration 300 --interval 0.5
# Run multiple simulators concurrently
```

## Troubleshooting

### Connection Issues

#### Problem: "Connection error" or "No response"
**Solution**: Ensure backend is running on port 8000
```bash
curl http://localhost:8000/health
```

#### Problem: Timeout errors
**Solution**: The simulator now auto-retries with exponential backoff. If retries fail:
1. Check if backend is running
2. Increase interval to reduce request frequency:
```bash
python drive_simulator.py --interval 2.0  # Slower updates
```
3. Check backend logs for errors
4. Verify backend isn't overloaded (check CPU usage)

#### Problem: Multiple retry attempts shown
**Cause**: Backend is temporarily overloaded or network is slow
**Solution**: This is normal behavior. The simulator will continue retrying automatically.
- Retry delays: 0.5s, 1.0s, 2.0s
- Maximum 3 attempts per request
- If all retries fail, request is skipped and simulation continues

### Backend Overload

#### Problem: Backend returns partial responses (confidence < 0.95)
**Cause**: Backend is processing too many concurrent requests (>10)
**Solution**: 
1. Reduce number of concurrent simulators
2. Increase update interval: `--interval 2.0`
3. Increase `MAX_CONCURRENT_REQUESTS` in `backend/main.py`:
```python
MAX_CONCURRENT_REQUESTS = 20  # Increase from 10
```

#### Problem: High response times (>1s)
**Cause**: Backend is busy processing multiple requests
**Solution**:
1. Check CPU usage on backend server
2. Ensure ML model is loaded (check startup logs)
3. Consider optimizing ML model or using rule-based scoring only

### Backend Issues

#### Problem: "ML service not initialized"
**Solution**: Check ML model file exists
```bash
ls -la ml_model/trained_model.pkl
```

#### Problem: NoneType errors
**Solution**: Backend now has automatic error recovery. Check logs for fallback to rule-based scoring.

### Simulation Issues

#### Problem: Unrealistic scores
**Solution**: This is expected! Different scenarios produce different scores:
- Cautious driving: 9-10
- Normal driving: 8-9
- Aggressive driving: 5-7

## Data Flow

```
┌──────────────┐
│  Simulator   │
│   (Python)   │
└──────┬───────┘
       │ HTTP POST
       │ /api/driving_data
       │ Every 1.0s
       ▼
┌──────────────┐
│   Backend    │◄──────┐
│   (FastAPI)  │       │ WebSocket
└──────┬───────┘       │ Real-time
       │               │
       │ Score         │
       │ Calculation   │
       │               │
       └───────────────┤
                       ▼
                ┌──────────────┐
                │  Dashboard   │
                │   (React)    │
                └──────────────┘
```

## Advanced Usage

### Multiple Fleet Simulations

Run multiple fleet simulations with different API URLs:

```bash
# Fleet Simulator 1
python drive_simulator.py --mode fleet --api-url http://localhost:8000/api

# Fleet Simulator 2 (on different backend)
python drive_simulator.py --mode fleet --api-url http://localhost:8001/api
```

### Continuous Testing

Use a loop for continuous testing:

```bash
#!/bin/bash
while true; do
    echo "Starting new simulation run..."
    python drive_simulator.py --duration 120 --mode personal
    sleep 5
done
```

### Custom Scenarios

Modify `drive_simulator.py` to adjust scenario probabilities:

```python
scenarios = [
    ('normal', 0.5),      # 50% normal
    ('highway', 0.2),     # 20% highway
    ('aggressive', 0.15), # 15% aggressive
    ('cautious', 0.1),    # 10% cautious
    ('emergency', 0.05)   # 5% emergency
]
```

## Integration with Dashboards

### Personal Dashboard
- Real-time telemetry charts
- Live safety score gauge
- AI-generated feedback
- Scenario indicator

### Fleet Dashboard
- Multi-driver tracking
- Driver rankings
- Fleet-level statistics
- AI-powered insights

Both dashboards automatically filter WebSocket messages by mode, so they show only relevant data.

## Best Practices

1. **Always start the backend first** before running simulators
2. **Use appropriate intervals** - 1.0s is recommended for demos
3. **Monitor backend logs** to see scoring method (ML or rule-based)
4. **Run short tests first** (30-60s) before long simulations
5. **Use different terminals** for concurrent simulations
6. **Check health endpoint** if experiencing issues

## Support

For issues or questions:
- Check backend logs: Look for error messages
- Check health endpoint: `curl http://localhost:8000/health`
- Review this guide: Ensure all prerequisites are met
- Open an issue on GitHub with logs and error messages

---

**Happy Simulating! 🚗💨**
