# Manual Testing Guide for Async Concurrency

This guide walks you through manually testing the parallel execution of Personal and Fleet simulators.

## Prerequisites

1. **Install Dependencies**
   ```bash
   # Backend dependencies
   cd backend
   pip install -r requirements.txt
   
   # Simulation dependencies
   cd ../simulation
   pip install -r requirements.txt
   ```

2. **Verify Async Implementation**
   ```bash
   cd ..
   python test_backend_validation.py
   python test_async_changes.py
   ```
   
   Both should show "✅ All tests passed!"

## Test 1: Backend Can Handle Concurrent Requests

### Start the Backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected output:**
```
🚀 Starting DriveMind.ai Backend...
✅ Services initialized successfully
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Verify Health Endpoint
In another terminal:
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "...",
  "services": {
    "ml_service": true,
    "supabase_service": true
  }
}
```

## Test 2: Run Personal Simulator Alone

In a second terminal:
```bash
cd simulation
python drive_simulator.py --mode personal --duration 30 --interval 1.0
```

**Expected output:**
```
🚗 Starting DriveMind.ai Driving Simulation (PERSONAL mode)
Session ID: <uuid>
Duration: 30s, Update interval: 1.0s
==================================================
📍 Scenario: normal
🚗 [PERSONAL] Speed:   60.5 km/h | Accel:  0.50 m/s² | Brake: 0.00 | Steer:   5.2° | Scenario: normal     | Score:  8.5/10 | Avg:  8.5/10 ✅
🚗 [PERSONAL] Speed:   62.3 km/h | Accel:  0.48 m/s² | Brake: 0.00 | Steer:   4.8° | Scenario: normal     | Score:  8.7/10 | Avg:  8.6/10 ✅
...
```

**✅ Success Criteria:**
- No timeout errors
- Each line shows a successful score: `| Score: X.X/10 | Avg: X.X/10 ✅`
- Simulation completes after 30 seconds

## Test 3: Run Fleet Simulator Alone

Stop the personal simulator (Ctrl+C), then:
```bash
python drive_simulator.py --mode fleet --duration 30 --interval 1.0
```

**Expected output:**
```
🚕 Starting DriveMind.ai Driving Simulation (FLEET mode)
Session ID: <uuid>
Duration: 30s, Update interval: 1.0s
==================================================
📍 Scenario: highway
🚕 [FLEET] Speed:   85.2 km/h | Accel:  1.20 m/s² | Brake: 0.00 | Steer:   2.1° | Scenario: highway    | Score:  7.8/10 | Avg:  7.8/10 ✅
🚕 [FLEET] Speed:   87.5 km/h | Accel:  1.15 m/s² | Brake: 0.00 | Steer:   1.9° | Scenario: highway    | Score:  7.9/10 | Avg:  7.85/10 ✅
...
```

**✅ Success Criteria:**
- Similar to personal mode
- Fleet emoji 🚕 shows instead of 🚗
- No timeout errors

## Test 4: 🎯 CRITICAL - Run Both Simulators Simultaneously

This is the main test for the async concurrency fix!

### Terminal 1: Backend (should already be running)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Terminal 2: Personal Simulator
```bash
cd simulation
python drive_simulator.py --mode personal --duration 60 --interval 1.0
```

### Terminal 3: Fleet Simulator (start within 5 seconds)
```bash
cd simulation
python drive_simulator.py --mode fleet --duration 60 --interval 1.0
```

### Watch Both Terminals Simultaneously

**✅ Success Criteria (BOTH simulators should show):**
1. Both simulators start successfully
2. Both show continuous score updates with ✅
3. **NO timeout errors** like these (which were the original problem):
   ```
   ⏳ Request timeout, retrying...
   ❌ Request timeout after 3 attempts
   ```
4. Both simulators complete after ~60 seconds
5. Backend terminal shows requests from both modes being processed

**Backend Terminal Should Show:**
```
INFO:     127.0.0.1:xxxxx - "POST /api/driving_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /api/driving_data HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /api/driving_data HTTP/1.1" 200 OK
...
```

## Test 5: Automated Parallel Test (Optional)

If you want to run the automated test:

```bash
# Make sure backend is running in another terminal
python test_parallel_simulators.py --duration 10
```

**Expected output:**
```
✅ Personal simulator completed successfully
✅ Fleet simulator completed successfully
⏱️  Total elapsed time: ~10s (expected ~10s)
✅ Execution timing is reasonable (simulators ran in parallel)
✅ PARALLEL EXECUTION TEST PASSED!
```

## Troubleshooting

### If you see timeout errors:
1. Check that backend is running and healthy
2. Verify aiohttp is installed: `pip install aiohttp==3.9.1`
3. Check backend logs for errors
4. Ensure you're using the updated async code

### If simulators run but backend errors:
1. Check backend terminal for Python exceptions
2. Verify all dependencies are installed
3. Check that ML model file exists (or rule-based scoring is used)

### If only one simulator works:
1. Check that both simulators are using different modes (personal vs fleet)
2. Verify WebSocket endpoints are configured correctly
3. Look for port conflicts

## Success Indicators

After running Test 4 successfully, you should see:

✅ **No timeout messages** in simulator output
✅ **Continuous score updates** with green checkmarks (✅)
✅ **Both simulators running simultaneously** without interference
✅ **Backend handling concurrent requests** (200 OK responses)
✅ **Independent session IDs** for each simulator
✅ **Completion after expected duration**

## Performance Metrics

With the async implementation, you should observe:

- **Response Time**: < 100ms per request (even with concurrent requests)
- **Throughput**: 10+ concurrent requests handled without degradation
- **No Blocking**: Both simulators send requests every 1 second without delays
- **Error Rate**: 0% (unless backend is actually down)

## Next Steps

If all tests pass:
1. ✅ Mark the PR as ready for review
2. ✅ Update any remaining documentation
3. ✅ Consider adding WebSocket tests for real-time dashboard updates

If any test fails:
1. Check the specific error messages
2. Review recent code changes
3. Verify dependencies are correctly installed
4. Check for any Python version compatibility issues
