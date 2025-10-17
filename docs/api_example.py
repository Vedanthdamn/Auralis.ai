"""
Example script showing how to use the DriveMind.ai API programmatically
"""
import requests
import json
from datetime import datetime

# API Base URL
API_URL = "http://localhost:8000/api"

def create_session(driver_id=None, vehicle_id=None):
    """Create a new driving session"""
    response = requests.post(
        f"{API_URL}/session",
        json={
            "driver_id": driver_id,
            "vehicle_id": vehicle_id
        }
    )
    return response.json()

def send_driving_data(speed, acceleration, braking_intensity, steering_angle, jerk=0.0):
    """Send driving data and get score"""
    data = {
        "speed": speed,
        "acceleration": acceleration,
        "braking_intensity": braking_intensity,
        "steering_angle": steering_angle,
        "jerk": jerk,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    response = requests.post(
        f"{API_URL}/driving_data",
        json=data
    )
    return response.json()

def get_current_score():
    """Get the current driving score"""
    response = requests.get(f"{API_URL}/current_score")
    return response.json()

def get_feedback(score, driving_data):
    """Get AI-generated feedback"""
    response = requests.post(
        f"{API_URL}/feedback",
        json={
            "score": score,
            "driving_data": driving_data
        }
    )
    return response.json()

def main():
    print("🚗 DriveMind.ai API Example")
    print("=" * 50)
    
    # Create a session
    print("\n1. Creating session...")
    session = create_session(driver_id="demo_driver", vehicle_id="demo_vehicle")
    print(f"   Session ID: {session['session_id']}")
    
    # Send some example driving data
    print("\n2. Sending driving data...")
    
    examples = [
        {
            "name": "Safe driving",
            "speed": 60.0,
            "acceleration": 0.5,
            "braking_intensity": 0.1,
            "steering_angle": 2.0,
            "jerk": 0.1
        },
        {
            "name": "Aggressive driving",
            "speed": 95.0,
            "acceleration": 3.5,
            "braking_intensity": 0.8,
            "steering_angle": 25.0,
            "jerk": 2.0
        },
        {
            "name": "Moderate driving",
            "speed": 70.0,
            "acceleration": 1.2,
            "braking_intensity": 0.3,
            "steering_angle": 8.0,
            "jerk": 0.5
        }
    ]
    
    for example in examples:
        print(f"\n   Testing: {example['name']}")
        result = send_driving_data(
            speed=example['speed'],
            acceleration=example['acceleration'],
            braking_intensity=example['braking_intensity'],
            steering_angle=example['steering_angle'],
            jerk=example['jerk']
        )
        print(f"   Score: {result['score']:.2f}/10")
    
    # Get current score
    print("\n3. Getting current score...")
    current = get_current_score()
    print(f"   Current score: {current['score']:.2f}/10")
    
    # Get feedback
    print("\n4. Getting AI feedback...")
    feedback = get_feedback(
        score=current['score'],
        driving_data={
            "speed": 70.0,
            "acceleration": 1.2,
            "braking_intensity": 0.3,
            "steering_angle": 8.0,
            "jerk": 0.5,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    print(f"   Feedback: {feedback['feedback']}")
    
    print("\n✅ Example complete!")

if __name__ == '__main__':
    main()
