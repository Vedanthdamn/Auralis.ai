from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
import asyncio
from datetime import datetime

from app.routes import router
from services.ml_service import MLService
from services.supabase_service import SupabaseService
from models.schemas import DrivingData

# Global services
ml_service = None
supabase_service = None

# Separate connection pools for personal and fleet dashboards
personal_connections = []
fleet_connections = []

# Concurrency control for handling multiple simulators
request_semaphore = None
MAX_CONCURRENT_REQUESTS = 10  # Allow up to 10 concurrent scoring requests

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize services
    global ml_service, supabase_service, request_semaphore
    print("🚀 Starting DriveMind.ai Backend...")
    
    # Initialize semaphore for concurrency control
    request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    # Update global variables (not local)
    ml_service = MLService()
    supabase_service = SupabaseService()
    
    # Update app state with initialized services
    app.state.ml_service = ml_service
    app.state.supabase_service = supabase_service
    app.state.request_semaphore = request_semaphore
    
    print("✅ Services initialized successfully")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down DriveMind.ai Backend...")

app = FastAPI(
    title="DriveMind.ai API",
    description="AI-Powered Driver Safety Scoring System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")

# WebSocket endpoint for personal dashboard
@app.websocket("/ws/personal")
async def personal_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    personal_connections.append(websocket)
    print(f"✅ Personal WebSocket client connected. Total personal connections: {len(personal_connections)}")
    
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back or process if needed
            await websocket.send_text(json.dumps({
                "type": "ack",
                "message": "Personal dashboard connected"
            }))
    except WebSocketDisconnect:
        personal_connections.remove(websocket)
        print(f"❌ Personal WebSocket client disconnected. Total personal connections: {len(personal_connections)}")
    except Exception as e:
        print(f"❌ Personal WebSocket error: {e}")
        if websocket in personal_connections:
            personal_connections.remove(websocket)

# WebSocket endpoint for fleet dashboard
@app.websocket("/ws/fleet")
async def fleet_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    fleet_connections.append(websocket)
    print(f"✅ Fleet WebSocket client connected. Total fleet connections: {len(fleet_connections)}")
    
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back or process if needed
            await websocket.send_text(json.dumps({
                "type": "ack",
                "message": "Fleet dashboard connected"
            }))
    except WebSocketDisconnect:
        fleet_connections.remove(websocket)
        print(f"❌ Fleet WebSocket client disconnected. Total fleet connections: {len(fleet_connections)}")
    except Exception as e:
        print(f"❌ Fleet WebSocket error: {e}")
        if websocket in fleet_connections:
            fleet_connections.remove(websocket)

# Legacy WebSocket endpoint (backward compatibility)
@app.websocket("/ws")
async def legacy_websocket_endpoint(websocket: WebSocket):
    """Legacy endpoint - broadcasts to both personal and fleet for backward compatibility"""
    await websocket.accept()
    personal_connections.append(websocket)
    print(f"⚠️ Legacy WebSocket client connected (will receive personal data). Total personal connections: {len(personal_connections)}")
    
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back or process if needed
            await websocket.send_text(json.dumps({
                "type": "ack",
                "message": "Message received (legacy endpoint)"
            }))
    except WebSocketDisconnect:
        personal_connections.remove(websocket)
        print(f"❌ Legacy WebSocket client disconnected. Total personal connections: {len(personal_connections)}")
    except Exception as e:
        print(f"❌ Legacy WebSocket error: {e}")
        if websocket in personal_connections:
            personal_connections.remove(websocket)

async def broadcast_to_clients(message: dict):
    """Broadcast message to appropriate WebSocket clients based on mode"""
    mode = message.get('mode', 'personal')
    
    # Select the appropriate connection pool
    if mode == 'fleet':
        connections = fleet_connections
        connection_type = "fleet"
    else:
        connections = personal_connections
        connection_type = "personal"
    
    disconnected = []
    for connection in connections:
        try:
            await connection.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error broadcasting to {connection_type} client: {e}")
            disconnected.append(connection)
    
    # Remove disconnected clients
    for conn in disconnected:
        if conn in connections:
            connections.remove(conn)

@app.get("/")
async def root():
    return {
        "message": "DriveMind.ai API is running",
        "version": "1.0.0",
        "status": "operational",
        "websocket_connections": {
            "personal": len(personal_connections),
            "fleet": len(fleet_connections),
            "total": len(personal_connections) + len(fleet_connections)
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "ml_service": ml_service is not None,
            "supabase_service": supabase_service is not None,
        }
    }

# Make broadcast available to routes
# Note: ml_service and supabase_service are set during lifespan startup
app.state.broadcast = broadcast_to_clients
