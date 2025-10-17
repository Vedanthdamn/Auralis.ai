"""
Sample Fleet Data Generator

This script generates sample fleet data for testing the fleet dashboard.
It creates drivers, vehicles, sessions, and events with realistic driving data.

Usage:
    python generate_fleet_data.py [--drivers N] [--sessions M]
    
    --drivers N: Number of drivers to create (default: 5)
    --sessions M: Number of sessions per driver (default: 10)
"""

import requests
import random
import time
import argparse
from datetime import datetime, timedelta
from typing import List, Dict

API_BASE_URL = "http://localhost:8000/api"

# Driver profiles
DRIVER_PROFILES = [
    {"driver_id": "DRV001", "name": "John Smith"},
    {"driver_id": "DRV002", "name": "Sarah Johnson"},
    {"driver_id": "DRV003", "name": "Michael Chen"},
    {"driver_id": "DRV004", "name": "Emily Davis"},
    {"driver_id": "DRV005", "name": "Robert Wilson"},
    {"driver_id": "DRV006", "name": "Jennifer Brown"},
    {"driver_id": "DRV007", "name": "David Martinez"},
    {"driver_id": "DRV008", "name": "Lisa Anderson"},
    {"driver_id": "DRV009", "name": "James Taylor"},
    {"driver_id": "DRV010", "name": "Maria Garcia"},
]

# Vehicle profiles
VEHICLE_PROFILES = [
    {"vehicle_id": "VEH001", "make": "Toyota", "model": "Camry"},
    {"vehicle_id": "VEH002", "make": "Honda", "model": "Accord"},
    {"vehicle_id": "VEH003", "make": "Tesla", "model": "Model 3"},
    {"vehicle_id": "VEH004", "make": "Ford", "model": "Fusion"},
    {"vehicle_id": "VEH005", "make": "Chevrolet", "model": "Malibu"},
    {"vehicle_id": "VEH006", "make": "Nissan", "model": "Altima"},
    {"vehicle_id": "VEH007", "make": "Hyundai", "model": "Sonata"},
    {"vehicle_id": "VEH008", "make": "Kia", "model": "Optima"},
    {"vehicle_id": "VEH009", "make": "Mazda", "model": "6"},
    {"vehicle_id": "VEH010", "make": "Subaru", "model": "Legacy"},
]

# Driving behavior profiles
BEHAVIOR_PROFILES = {
    "excellent": {
        "speed_range": (40, 70),
        "acceleration_range": (0.3, 1.2),
        "braking_range": (0.1, 0.3),
        "steering_range": (0, 10),
        "score_avg": 8.5,
    },
    "good": {
        "speed_range": (45, 80),
        "acceleration_range": (0.5, 2.0),
        "braking_range": (0.2, 0.5),
        "steering_range": (0, 15),
        "score_avg": 7.0,
    },
    "average": {
        "speed_range": (50, 90),
        "acceleration_range": (0.8, 2.5),
        "braking_range": (0.3, 0.6),
        "steering_range": (0, 20),
        "score_avg": 5.5,
    },
    "poor": {
        "speed_range": (60, 110),
        "acceleration_range": (1.5, 3.5),
        "braking_range": (0.5, 0.8),
        "steering_range": (10, 30),
        "score_avg": 3.5,
    },
}


def generate_driving_event(behavior: str) -> Dict:
    """Generate a single driving event based on behavior profile"""
    profile = BEHAVIOR_PROFILES[behavior]
    
    speed = random.uniform(*profile["speed_range"])
    acceleration = random.uniform(*profile["acceleration_range"]) * random.choice([1, -1])
    braking_intensity = random.uniform(*profile["braking_range"])
    steering_angle = random.uniform(*profile["steering_range"]) * random.choice([1, -1])
    jerk = random.uniform(0, 1.0)
    
    return {
        "speed": round(speed, 2),
        "acceleration": round(acceleration, 2),
        "braking_intensity": round(braking_intensity, 2),
        "steering_angle": round(steering_angle, 2),
        "jerk": round(jerk, 2),
        "timestamp": datetime.utcnow().isoformat(),
    }


def create_session(driver_id: str, vehicle_id: str) -> str:
    """Create a driving session"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/session",
            json={
                "driver_id": driver_id,
                "vehicle_id": vehicle_id,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("session_id")
    except Exception as e:
        print(f"Error creating session: {e}")
        return None


def send_driving_data(event: Dict) -> float:
    """Send driving data to the API and get the score"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/driving_data",
            json=event,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("score")
    except Exception as e:
        print(f"Error sending driving data: {e}")
        return None


def simulate_trip(driver_id: str, vehicle_id: str, behavior: str, duration: int = 60):
    """Simulate a complete trip with multiple data points"""
    print(f"  Simulating {behavior} trip for {driver_id}...")
    
    # Create session
    session_id = create_session(driver_id, vehicle_id)
    if not session_id:
        print(f"  Failed to create session for {driver_id}")
        return
    
    scores = []
    events_per_trip = duration // 5  # One event every 5 seconds
    
    for i in range(events_per_trip):
        event = generate_driving_event(behavior)
        score = send_driving_data(event)
        
        if score is not None:
            scores.append(score)
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.1)
    
    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"  Trip completed. Average score: {avg_score:.2f}")
    
    return avg_score


def generate_fleet_data(num_drivers: int = 5, sessions_per_driver: int = 10):
    """Generate complete fleet data"""
    print(f"Generating fleet data for {num_drivers} drivers...")
    print(f"Each driver will have {sessions_per_driver} sessions")
    print("-" * 60)
    
    # Select drivers and vehicles
    drivers = DRIVER_PROFILES[:num_drivers]
    vehicles = VEHICLE_PROFILES[:num_drivers]
    
    # Assign behavior profiles to drivers (mix of behaviors)
    behaviors = ["excellent", "excellent", "good", "good", "average", "average", "poor"]
    driver_behaviors = {}
    
    for i, driver in enumerate(drivers):
        # Assign a primary behavior with some variation
        primary_behavior = random.choice(behaviors)
        driver_behaviors[driver["driver_id"]] = primary_behavior
        print(f"Driver {driver['name']} ({driver['driver_id']}): {primary_behavior.upper()} driver")
    
    print("-" * 60)
    
    # Generate sessions for each driver
    for driver in drivers:
        driver_id = driver["driver_id"]
        driver_name = driver["name"]
        vehicle = random.choice(vehicles)
        behavior = driver_behaviors[driver_id]
        
        print(f"\nGenerating {sessions_per_driver} sessions for {driver_name}...")
        
        for session_num in range(1, sessions_per_driver + 1):
            print(f"Session {session_num}/{sessions_per_driver}:")
            
            # Occasionally vary the behavior slightly
            if random.random() < 0.2:  # 20% chance of variation
                behaviors_list = list(BEHAVIOR_PROFILES.keys())
                behavior_index = behaviors_list.index(behavior)
                # Shift behavior up or down by one level
                if behavior_index > 0 and random.random() < 0.5:
                    varied_behavior = behaviors_list[behavior_index - 1]
                elif behavior_index < len(behaviors_list) - 1:
                    varied_behavior = behaviors_list[behavior_index + 1]
                else:
                    varied_behavior = behavior
            else:
                varied_behavior = behavior
            
            # Simulate trip
            simulate_trip(
                driver_id=driver_id,
                vehicle_id=vehicle["vehicle_id"],
                behavior=varied_behavior,
                duration=random.randint(30, 120),  # 30 seconds to 2 minutes
            )
            
            time.sleep(0.5)  # Pause between trips
    
    print("\n" + "=" * 60)
    print("Fleet data generation complete!")
    print("=" * 60)
    print(f"\nYou can now view the fleet dashboard at:")
    print("http://localhost:3000/dashboard/fleet")


def main():
    parser = argparse.ArgumentParser(
        description="Generate sample fleet data for Auralis.ai"
    )
    parser.add_argument(
        "--drivers",
        type=int,
        default=5,
        help="Number of drivers to create (default: 5, max: 10)",
    )
    parser.add_argument(
        "--sessions",
        type=int,
        default=10,
        help="Number of sessions per driver (default: 10)",
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    num_drivers = min(max(1, args.drivers), 10)
    sessions_per_driver = max(1, args.sessions)
    
    if num_drivers != args.drivers:
        print(f"Note: Number of drivers capped at 10 (requested: {args.drivers})")
    
    try:
        # Test API connection
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}/health", timeout=5)
        response.raise_for_status()
        print("✅ Backend API is running")
    except Exception as e:
        print(f"❌ Error: Backend API is not accessible at {API_BASE_URL}")
        print(f"   Please make sure the backend is running on port 8000")
        print(f"   Error: {e}")
        return
    
    # Generate data
    generate_fleet_data(num_drivers, sessions_per_driver)


if __name__ == "__main__":
    main()
