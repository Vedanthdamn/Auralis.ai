from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DrivingData(BaseModel):
    """Real-time driving telemetry data"""
    speed: float = Field(..., description="Current speed in km/h")
    acceleration: float = Field(..., description="Current acceleration in m/s²")
    braking_intensity: float = Field(..., ge=0, le=1, description="Braking intensity (0-1)")
    steering_angle: float = Field(..., description="Steering angle in degrees")
    jerk: Optional[float] = Field(None, description="Rate of change of acceleration")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "speed": 60.5,
                "acceleration": 0.5,
                "braking_intensity": 0.0,
                "steering_angle": 5.2,
                "jerk": 0.1,
                "timestamp": "2024-01-01T12:00:00"
            }
        }

class ScoreResponse(BaseModel):
    """Driving safety score response"""
    score: float = Field(..., ge=0, le=10, description="Safety score (0-10)")
    timestamp: datetime
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Model confidence")

class FeedbackRequest(BaseModel):
    """Request for AI-generated feedback"""
    score: float
    driving_data: DrivingData
    session_id: Optional[str] = None

class FeedbackResponse(BaseModel):
    """AI-generated feedback response"""
    feedback: str
    timestamp: datetime

class SessionCreate(BaseModel):
    """Create new driving session"""
    driver_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    
class SessionResponse(BaseModel):
    """Driving session response"""
    session_id: str
    start_time: datetime
    driver_id: Optional[str]
    vehicle_id: Optional[str]
