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
        # Return sample data when database is not configured
        return {
            "total_drivers": 5,
            "total_trips": 120,
            "fleet_avg_score": 7.5,
            "safest_driver": "John Doe",
            "safest_driver_score": 9.2,
            "most_improved_driver": "Jane Smith",
            "most_improved_score": 8.1,
            "high_performers": 2,
            "average_performers": 2,
            "low_performers": 1
        }
    
    try:
        summary = await supabase_service.get_fleet_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting fleet summary: {str(e)}")

@router.get("/fleet/drivers")
async def get_fleet_drivers(request: Request, include_feedback: bool = False):
    """
    Get list of all drivers with their statistics and rankings
    
    Args:
        include_feedback: If True, generates AI feedback for each driver (slower but more complete)
    """
    supabase_service = request.app.state.supabase_service
    ml_service = request.app.state.ml_service
    
    if not supabase_service.is_configured():
        # Return sample data when database is not configured
        sample_drivers = [
            {
                "driver_id": "DRV001",
                "driver_name": "John Doe",
                "avg_score": 9.2,
                "trip_count": 45,
                "best_score": 9.8,
                "worst_score": 8.5,
                "last_trip_date": "2024-01-15T10:30:00",
                "avg_speed": 62.5,
                "avg_acceleration": 1.2,
                "avg_braking": 0.3,
                "rank": 1
            },
            {
                "driver_id": "DRV002",
                "driver_name": "Jane Smith",
                "avg_score": 8.1,
                "trip_count": 38,
                "best_score": 9.0,
                "worst_score": 6.8,
                "last_trip_date": "2024-01-14T15:20:00",
                "avg_speed": 65.2,
                "avg_acceleration": 1.5,
                "avg_braking": 0.4,
                "rank": 2
            },
            {
                "driver_id": "DRV003",
                "driver_name": "Bob Johnson",
                "avg_score": 7.5,
                "trip_count": 52,
                "best_score": 8.2,
                "worst_score": 6.5,
                "last_trip_date": "2024-01-15T09:45:00",
                "avg_speed": 68.0,
                "avg_acceleration": 1.8,
                "avg_braking": 0.5,
                "rank": 3
            },
            {
                "driver_id": "DRV004",
                "driver_name": "Alice Brown",
                "avg_score": 6.8,
                "trip_count": 29,
                "best_score": 7.5,
                "worst_score": 5.8,
                "last_trip_date": "2024-01-13T14:10:00",
                "avg_speed": 70.5,
                "avg_acceleration": 2.1,
                "avg_braking": 0.6,
                "rank": 4
            },
            {
                "driver_id": "DRV005",
                "driver_name": "Charlie Davis",
                "avg_score": 5.9,
                "trip_count": 31,
                "best_score": 6.9,
                "worst_score": 4.8,
                "last_trip_date": "2024-01-12T11:30:00",
                "avg_speed": 75.0,
                "avg_acceleration": 2.5,
                "avg_braking": 0.7,
                "rank": 5
            }
        ]
        return {
            "drivers": sample_drivers,
            "total_count": len(sample_drivers)
        }
    
    try:
        driver_stats = await supabase_service.get_driver_stats()
        
        # Sort by avg_score and add rankings
        driver_stats.sort(key=lambda x: x.get('avg_score', 0), reverse=True)
        
        for idx, driver in enumerate(driver_stats, start=1):
            driver['rank'] = idx
            
            # Optionally include AI feedback for each driver
            if include_feedback:
                try:
                    feedback = await ml_service.generate_driver_feedback(driver)
                    driver['ai_feedback'] = feedback
                except Exception as e:
                    print(f"Failed to generate feedback for driver {driver.get('driver_id')}: {e}")
                    driver['ai_feedback'] = None
        
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
        # Use sample data when database is not configured
        sample_drivers = {
            "DRV001": {
                "driver_id": "DRV001",
                "driver_name": "John Doe",
                "avg_score": 9.2,
                "trip_count": 45,
                "avg_speed": 62.5,
                "avg_acceleration": 1.2,
                "avg_braking": 0.3
            },
            "DRV002": {
                "driver_id": "DRV002",
                "driver_name": "Jane Smith",
                "avg_score": 8.1,
                "trip_count": 38,
                "avg_speed": 65.2,
                "avg_acceleration": 1.5,
                "avg_braking": 0.4
            },
            "DRV003": {
                "driver_id": "DRV003",
                "driver_name": "Bob Johnson",
                "avg_score": 7.5,
                "trip_count": 52,
                "avg_speed": 68.0,
                "avg_acceleration": 1.8,
                "avg_braking": 0.5
            },
            "DRV004": {
                "driver_id": "DRV004",
                "driver_name": "Alice Brown",
                "avg_score": 6.8,
                "trip_count": 29,
                "avg_speed": 70.5,
                "avg_acceleration": 2.1,
                "avg_braking": 0.6
            },
            "DRV005": {
                "driver_id": "DRV005",
                "driver_name": "Charlie Davis",
                "avg_score": 5.9,
                "trip_count": 31,
                "avg_speed": 75.0,
                "avg_acceleration": 2.5,
                "avg_braking": 0.7
            }
        }
        
        if driver_id not in sample_drivers:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        driver_stats = sample_drivers[driver_id]
        feedback = await ml_service.generate_driver_feedback(driver_stats)
        
        return {
            "driver_id": driver_id,
            "driver_name": driver_stats.get('driver_name', driver_id),
            "feedback": feedback,
            "score": driver_stats.get('avg_score', 0),
            "timestamp": datetime.utcnow()
        }
    
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
        # Return sample insights when database is not configured
        sample_summary = {
            "total_drivers": 5,
            "total_trips": 120,
            "fleet_avg_score": 7.5,
            "safest_driver": "John Doe",
            "safest_driver_score": 9.2
        }
        sample_drivers = [
            {"driver_id": "DRV001", "avg_score": 9.2},
            {"driver_id": "DRV002", "avg_score": 8.1},
            {"driver_id": "DRV003", "avg_score": 7.5},
            {"driver_id": "DRV004", "avg_score": 6.8},
            {"driver_id": "DRV005", "avg_score": 5.9}
        ]
        
        # Generate insights even with sample data
        insights = await ml_service.generate_fleet_insights(sample_summary, sample_drivers)
        
        return {
            "insights": insights,
            "timestamp": datetime.utcnow(),
            "fleet_summary": sample_summary
        }
    
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
