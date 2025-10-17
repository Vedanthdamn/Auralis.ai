from fastapi import APIRouter, HTTPException, Request
from datetime import datetime
from models.schemas import (
    DrivingData, 
    ScoreResponse, 
    FeedbackRequest, 
    FeedbackResponse,
    SessionCreate,
    SessionResponse
)
import uuid

router = APIRouter()

@router.post("/driving_data", response_model=ScoreResponse)
async def receive_driving_data(data: DrivingData, request: Request):
    """
    Receive driving data and calculate safety score
    """
    try:
        # Get ML service from app state
        ml_service = request.app.state.ml_service
        
        # Calculate driving score
        score = ml_service.calculate_score(data)
        
        # Broadcast to WebSocket clients
        broadcast = request.app.state.broadcast
        await broadcast({
            "type": "driving_data",
            "payload": data.model_dump(mode='json')
        })
        
        await broadcast({
            "type": "score_update",
            "payload": {
                "score": score,
                "timestamp": datetime.utcnow().isoformat()
            }
        })
        
        # Store in database if Supabase is configured
        supabase_service = request.app.state.supabase_service
        if supabase_service.is_configured():
            try:
                await supabase_service.store_event(data, score)
            except Exception as e:
                print(f"Failed to store in Supabase: {e}")
        
        return ScoreResponse(
            score=score,
            timestamp=datetime.utcnow(),
            confidence=0.95
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current_score", response_model=ScoreResponse)
async def get_current_score(request: Request):
    """
    Get the current driving score
    """
    ml_service = request.app.state.ml_service
    current_score = ml_service.get_last_score()
    
    if current_score is None:
        raise HTTPException(status_code=404, detail="No score available yet")
    
    return ScoreResponse(
        score=current_score,
        timestamp=datetime.utcnow(),
        confidence=0.95
    )

@router.post("/feedback", response_model=FeedbackResponse)
async def get_feedback(feedback_req: FeedbackRequest, request: Request):
    """
    Generate AI feedback based on driving data and score
    """
    try:
        ml_service = request.app.state.ml_service
        
        # Generate feedback (use Ollama if available)
        feedback = await ml_service.generate_feedback(
            feedback_req.score, 
            feedback_req.driving_data
        )
        
        # Broadcast to WebSocket clients
        broadcast = request.app.state.broadcast
        await broadcast({
            "type": "feedback",
            "payload": {
                "feedback": feedback,
                "timestamp": datetime.utcnow().isoformat()
            }
        })
        
        return FeedbackResponse(
            feedback=feedback,
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session", response_model=SessionResponse)
async def create_session(session: SessionCreate, request: Request):
    """
    Create a new driving session
    """
    session_id = str(uuid.uuid4())
    
    supabase_service = request.app.state.supabase_service
    if supabase_service.is_configured():
        try:
            await supabase_service.create_session(
                session_id, 
                session.driver_id, 
                session.vehicle_id
            )
        except Exception as e:
            print(f"Failed to create session in Supabase: {e}")
    
    return SessionResponse(
        session_id=session_id,
        start_time=datetime.utcnow(),
        driver_id=session.driver_id,
        vehicle_id=session.vehicle_id
    )

@router.get("/sessions/{session_id}")
async def get_session(session_id: str, request: Request):
    """
    Get session details and history
    """
    supabase_service = request.app.state.supabase_service
    
    if not supabase_service.is_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        session_data = await supabase_service.get_session(session_id)
        return session_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Session not found: {str(e)}")
