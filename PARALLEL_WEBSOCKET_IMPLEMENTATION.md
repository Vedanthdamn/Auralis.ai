# Parallel WebSocket Implementation

## Overview

This document describes the implementation of parallel WebSocket streaming for personal and fleet dashboards in DriveMind.ai.

## Problem Statement

Previously, when switching between the personal and fleet dashboards, only one would receive live driving data at a time. The other would show "connected" but receive no transmission, with the backend logs showing request timeouts.

## Root Cause

Both dashboards were connecting to the same WebSocket endpoint (`/ws`) and receiving the same broadcast stream. The frontend attempted to filter messages by `mode`, but this created race conditions and data conflicts.

## Solution

Implemented **separate WebSocket endpoints** with **independent connection pools** for each dashboard type:

### Backend Changes (main.py)

1. **Separate Connection Pools**
   ```python
   personal_connections = []  # For personal dashboard
   fleet_connections = []     # For fleet dashboard
   ```

2. **Dedicated WebSocket Endpoints**
   - `/ws/personal` - Personal dashboard endpoint
   - `/ws/fleet` - Fleet dashboard endpoint
   - `/ws` - Legacy endpoint (backward compatible, routes to personal)

3. **Smart Broadcasting**
   ```python
   async def broadcast_to_clients(message: dict):
       mode = message.get('mode', 'personal')
       
       # Route to appropriate connection pool
       if mode == 'fleet':
           connections = fleet_connections
       else:
           connections = personal_connections
       
       # Broadcast to selected pool
       for connection in connections:
           await connection.send_text(json.dumps(message))
   ```

### Frontend Changes (App.jsx)

1. **Personal Dashboard**
   - Connects to: `ws://localhost:8000/ws/personal`
   - Processes all messages from personal endpoint
   - No filtering needed

2. **Fleet Dashboard**
   - Connects to: `ws://localhost:8000/ws/fleet`
   - Processes all messages from fleet endpoint
   - No filtering needed

### Simulator Compatibility

The existing simulator code already includes `simulation_mode` field in telemetry data, so it works seamlessly with the new implementation:

```python
telemetry = {
    'speed': 60.5,
    'simulation_mode': 'personal',  # or 'fleet'
    # ... other fields
}
```

The backend automatically routes broadcasts to the correct WebSocket endpoint based on this field.

## Architecture

```
┌──────────────────┐   /ws/personal    ┌──────────────────┐
│ Personal         │◄─────────────────►│                  │
│ Dashboard        │                    │                  │
└──────────────────┘                    │  FastAPI Backend │
                                        │                  │
┌──────────────────┐   /ws/fleet       │  - /ws/personal  │
│ Fleet            │◄─────────────────►│  - /ws/fleet     │
│ Dashboard        │                    │  - /ws (legacy)  │
└──────────────────┘                    └──────────────────┘
```

## Benefits

1. **True Parallel Streaming**: Both dashboards receive data simultaneously
2. **No Data Crosstalk**: Personal and fleet data streams are completely isolated
3. **Independent Connections**: Each dashboard maintains its own WebSocket connection
4. **Backward Compatible**: Legacy `/ws` endpoint still works
5. **Scalable**: Easy to add more dashboard types in the future
6. **Cleaner Code**: No complex filtering logic in frontend

## Testing

### Automated Tests

Created `test_parallel_websockets.py` with 6 test cases:

1. ✅ Root Endpoint - Verify connection tracking
2. ✅ Personal WebSocket - Test `/ws/personal` endpoint
3. ✅ Fleet WebSocket - Test `/ws/fleet` endpoint
4. ✅ Legacy WebSocket - Test `/ws` backward compatibility
5. ✅ Parallel WebSockets - Test simultaneous connections
6. ✅ Driving Data Routing - Test data routing to correct endpoints

**Result**: All tests passing (6/6)

### Manual Testing

1. Started backend server
2. Ran both personal and fleet simulators simultaneously
3. Verified both sent data successfully
4. Confirmed backend tracked connections separately
5. Validated no interference between simulators

**Result**: Both simulators ran successfully in parallel with correct data routing

## Usage

### Running Both Dashboards in Parallel

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

Open both dashboards in browser:
- Personal: `http://localhost:3000/dashboard`
- Fleet: `http://localhost:3000/dashboard/fleet`

Both will receive live data simultaneously without interference.

## Migration Guide

### For Existing Deployments

No breaking changes! The implementation is backward compatible:

1. Legacy `/ws` endpoint still works (routes to personal)
2. Existing simulators work without modification (already send `simulation_mode`)
3. Frontend changes are isolated to connection URLs

### For New Implementations

Use the dedicated endpoints:
- Personal dashboard → `ws://your-host:8000/ws/personal`
- Fleet dashboard → `ws://your-host:8000/ws/fleet`

## Performance Considerations

- **Memory**: Separate connection pools use minimal additional memory
- **CPU**: Broadcasting is still O(n) where n = connections in target pool
- **Network**: No overhead - only sends data to relevant connections
- **Concurrency**: Backend handles up to 10 concurrent requests (configurable)

## Future Enhancements

Potential improvements for future versions:

1. **Connection Authentication**: Add token-based auth for WebSocket connections
2. **Message Filtering**: Allow clients to subscribe to specific data types
3. **Connection Pooling**: Implement connection limits per dashboard type
4. **Metrics**: Add Prometheus/Grafana metrics for WebSocket health
5. **Load Balancing**: Support multiple backend instances with Redis pub/sub

## Conclusion

The parallel WebSocket implementation successfully resolves the issue of simultaneous dashboard access. Both personal and fleet dashboards can now receive real-time driving data without interference, improving the overall user experience and system reliability.
