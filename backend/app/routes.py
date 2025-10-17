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
        
        # Check if ML service is available
        if ml_service is None:
            raise HTTPException(
                status_code=503, 
                detail="ML service not initialized. Please check server logs."
            )
        
        # Calculate driving score with error handling
        try:
            score = ml_service.calculate_score(data)
        except AttributeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calculating score: ML service not properly initialized - {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calculating score: {str(e)}"
            )
        
        # Broadcast to WebSocket clients
        try:
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
        except Exception as e:
            # Log but don't fail the request if broadcasting fails
            print(f"Warning: Failed to broadcast to WebSocket clients: {e}")
        
        # Store in database if Supabase is configured
        try:
            supabase_service = request.app.state.supabase_service
            if supabase_service and supabase_service.is_configured():
                await supabase_service.store_event(data, score)
        except Exception as e:
            # Log but don't fail the request if Supabase storage fails
            print(f"Warning: Failed to store in Supabase: {e}")
        
        return ScoreResponse(
            score=score,
            timestamp=datetime.utcnow(),
            confidence=0.95
        )
    
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error processing driving data: {str(e)}"
        )

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

# Fleet Management Endpoints

@router.get("/fleet/summary")
async def get_fleet_summary(request: Request):
    """
    Get fleet-level summary statistics
    """
    supabase_service = request.app.state.supabase_service
    
    if not supabase_service.is_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        summary = await supabase_service.get_fleet_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting fleet summary: {str(e)}")

@router.get("/fleet/drivers")
async def get_fleet_drivers(request: Request):
    """
    Get list of all drivers with their statistics and rankings
    """
    supabase_service = request.app.state.supabase_service
    
    if not supabase_service.is_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        driver_stats = await supabase_service.get_driver_stats()
        
        # Sort by avg_score and add rankings
        driver_stats.sort(key=lambda x: x.get('avg_score', 0), reverse=True)
        
        for idx, driver in enumerate(driver_stats, start=1):
            driver['rank'] = idx
        
        return {
            "drivers": driver_stats,
            "total_count": len(driver_stats)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting fleet drivers: {str(e)}")

@router.get("/fleet/drivers/{driver_id}")
async def get_driver_details(driver_id: str, request: Request):
    """
    Get detailed information for a specific driver
    """
    supabase_service = request.app.state.supabase_service
    
    if not supabase_service.is_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        # Get driver profile
        driver_profile = await supabase_service.get_driver(driver_id)
        
        # Get driver statistics
        driver_stats_list = await supabase_service.get_driver_stats(driver_id)
        driver_stats = driver_stats_list[0] if driver_stats_list else None
        
        if not driver_profile and not driver_stats:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        return {
            "profile": driver_profile,
            "stats": driver_stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting driver details: {str(e)}")

@router.post("/fleet/drivers/{driver_id}/feedback")
async def generate_driver_feedback(driver_id: str, request: Request):
    """
    Generate AI feedback for a specific driver based on their performance
    """
    supabase_service = request.app.state.supabase_service
    ml_service = request.app.state.ml_service
    
    if not supabase_service.is_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        # Get driver statistics
        driver_stats_list = await supabase_service.get_driver_stats(driver_id)
        
        if not driver_stats_list:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        driver_stats = driver_stats_list[0]
        
        # Generate feedback
        feedback = await ml_service.generate_driver_feedback(driver_stats)
        
        return {
            "driver_id": driver_id,
            "driver_name": driver_stats.get('driver_name', driver_id),
            "feedback": feedback,
            "score": driver_stats.get('avg_score', 0),
            "timestamp": datetime.utcnow()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating driver feedback: {str(e)}")

@router.get("/fleet/insights")
async def get_fleet_insights(request: Request):
    """
    Get AI-generated insights for the entire fleet
    """
    supabase_service = request.app.state.supabase_service
    ml_service = request.app.state.ml_service
    
    if not supabase_service.is_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        # Get fleet summary and driver stats
        fleet_summary = await supabase_service.get_fleet_summary()
        driver_stats = await supabase_service.get_driver_stats()
        
        # Generate insights
        insights = await ml_service.generate_fleet_insights(fleet_summary, driver_stats)
        
        return {
            "insights": insights,
            "timestamp": datetime.utcnow(),
            "fleet_summary": fleet_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating fleet insights: {str(e)}")
