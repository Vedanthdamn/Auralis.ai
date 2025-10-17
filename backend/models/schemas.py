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
    simulation_mode: Optional[str] = Field(None, description="Simulation mode: 'personal' or 'fleet'")
    scenario: Optional[str] = Field(None, description="Current driving scenario")
    session_id: Optional[str] = Field(None, description="Session ID for tracking separate simulation runs")
    
    class Config:
        json_schema_extra = {
            "example": {
                "speed": 60.5,
                "acceleration": 0.5,
                "braking_intensity": 0.0,
                "steering_angle": 5.2,
                "jerk": 0.1,
                "timestamp": "2024-01-01T12:00:00",
                "simulation_mode": "personal",
                "scenario": "normal",
                "session_id": "550e8400-e29b-41d4-a716-446655440000"
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

# Fleet Management Schemas

class DriverProfile(BaseModel):
    """Driver profile information"""
    driver_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None

class VehicleProfile(BaseModel):
    """Vehicle profile information"""
    vehicle_id: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None

class DriverStats(BaseModel):
    """Driver statistics for fleet dashboard"""
    driver_id: str
    driver_name: str
    avg_score: float
    trip_count: int
    best_score: Optional[float] = None
    worst_score: Optional[float] = None
    last_trip_date: Optional[datetime] = None
    rank: Optional[int] = None

class FleetSummary(BaseModel):
    """Fleet-level summary statistics"""
    total_drivers: int
    total_trips: int
    fleet_avg_score: float
    safest_driver: Optional[str] = None
    safest_driver_score: Optional[float] = None
    most_improved_driver: Optional[str] = None

class DriverFeedback(BaseModel):
    """AI-generated feedback for a driver"""
    driver_id: str
    driver_name: str
    feedback: str
    score: float
    timestamp: datetime
