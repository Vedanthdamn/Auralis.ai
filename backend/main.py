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
active_connections = []

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

# WebSocket endpoint for real-time data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"✅ WebSocket client connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back or process if needed
            await websocket.send_text(json.dumps({
                "type": "ack",
                "message": "Message received"
            }))
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"❌ WebSocket client disconnected. Total connections: {len(active_connections)}")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

async def broadcast_to_clients(message: dict):
    """Broadcast message to all connected WebSocket clients"""
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error broadcasting to client: {e}")
            disconnected.append(connection)
    
    # Remove disconnected clients
    for conn in disconnected:
        if conn in active_connections:
            active_connections.remove(conn)

@app.get("/")
async def root():
    return {
        "message": "DriveMind.ai API is running",
        "version": "1.0.0",
        "status": "operational",
        "websocket_connections": len(active_connections)
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
