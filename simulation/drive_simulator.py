"""
Realistic driving simulation that generates telemetry data
and sends it to the backend API in real-time
"""
import numpy as np
import time
import requests
import json
from datetime import datetime
from typing import Dict, Optional

class DrivingSimulator:
    """
    Simulates realistic driving behavior with various scenarios:
    - Normal city driving
    - Highway driving
    - Aggressive driving
    - Emergency situations
    """
    
    def __init__(self, api_url: str = "http://localhost:8000/api"):
        self.api_url = api_url
        self.time_step = 0.1  # 100ms update rate
        
        # Current state
        self.speed = 0.0  # km/h
        self.acceleration = 0.0  # m/s²
        self.braking_intensity = 0.0  # 0-1
        self.steering_angle = 0.0  # degrees
        self.jerk = 0.0  # m/s³
        
        # Scenario parameters
        self.scenario = 'normal'
        self.target_speed = 60.0
        
    def update_physics(self, dt: float):
        """Update vehicle physics"""
        # Convert km/h to m/s for calculations
        speed_ms = self.speed / 3.6
        
        # Update speed based on acceleration
        speed_ms += self.acceleration * dt
        
        # Apply braking
        if self.braking_intensity > 0:
            brake_deceleration = -8.0 * self.braking_intensity  # Max ~8 m/s² braking
            speed_ms += brake_deceleration * dt
        
        # Ensure speed doesn't go negative
        speed_ms = max(0, speed_ms)
        
        # Convert back to km/h
        self.speed = speed_ms * 3.6
        
        # Steering tends to return to center
        self.steering_angle *= 0.95
        
    def select_random_scenario(self):
        """Randomly select a driving scenario"""
        scenarios = [
            ('normal', 0.5),
            ('highway', 0.2),
            ('aggressive', 0.15),
            ('cautious', 0.1),
            ('emergency', 0.05)
        ]
        
        scenario_names = [s[0] for s in scenarios]
        probabilities = [s[1] for s in scenarios]
        
        self.scenario = np.random.choice(scenario_names, p=probabilities)
        
        # Set target speed based on scenario
        if self.scenario == 'normal':
            self.target_speed = np.random.uniform(40, 70)
        elif self.scenario == 'highway':
            self.target_speed = np.random.uniform(80, 110)
        elif self.scenario == 'aggressive':
            self.target_speed = np.random.uniform(70, 100)
        elif self.scenario == 'cautious':
            self.target_speed = np.random.uniform(30, 50)
        elif self.scenario == 'emergency':
            self.target_speed = 0  # Emergency stop
    
    def generate_driving_behavior(self):
        """Generate realistic driving behavior based on scenario"""
        if self.scenario == 'normal':
            # Smooth acceleration/deceleration
            if self.speed < self.target_speed:
                self.acceleration = np.random.uniform(0.5, 1.5)
                self.braking_intensity = 0
            elif self.speed > self.target_speed:
                self.acceleration = 0
                self.braking_intensity = np.random.uniform(0.1, 0.3)
            else:
                self.acceleration = np.random.uniform(-0.2, 0.2)
                self.braking_intensity = 0
            
            # Gentle steering
            self.steering_angle += np.random.uniform(-2, 2)
            self.steering_angle = np.clip(self.steering_angle, -15, 15)
            
        elif self.scenario == 'highway':
            # Steady speed with minimal steering
            if self.speed < self.target_speed:
                self.acceleration = np.random.uniform(1.0, 2.0)
                self.braking_intensity = 0
            elif self.speed > self.target_speed:
                self.acceleration = 0
                self.braking_intensity = np.random.uniform(0.1, 0.2)
            else:
                self.acceleration = np.random.uniform(-0.1, 0.1)
                self.braking_intensity = 0
            
            # Minimal steering on highway
            self.steering_angle += np.random.uniform(-1, 1)
            self.steering_angle = np.clip(self.steering_angle, -5, 5)
            
        elif self.scenario == 'aggressive':
            # Hard acceleration and braking
            if self.speed < self.target_speed:
                self.acceleration = np.random.uniform(2.0, 4.0)
                self.braking_intensity = 0
            else:
                self.acceleration = 0
                self.braking_intensity = np.random.uniform(0.5, 0.9)
            
            # Sharp steering
            self.steering_angle += np.random.uniform(-5, 5)
            self.steering_angle = np.clip(self.steering_angle, -30, 30)
            
        elif self.scenario == 'cautious':
            # Very gentle driving
            if self.speed < self.target_speed:
                self.acceleration = np.random.uniform(0.2, 0.8)
                self.braking_intensity = 0
            elif self.speed > self.target_speed:
                self.acceleration = 0
                self.braking_intensity = np.random.uniform(0.05, 0.15)
            
            # Minimal steering
            self.steering_angle += np.random.uniform(-1, 1)
            self.steering_angle = np.clip(self.steering_angle, -10, 10)
            
        elif self.scenario == 'emergency':
            # Emergency braking
            self.acceleration = 0
            self.braking_intensity = np.random.uniform(0.8, 1.0)
            
            # Possible evasive steering
            if np.random.random() < 0.3:
                self.steering_angle += np.random.uniform(-10, 10)
                self.steering_angle = np.clip(self.steering_angle, -40, 40)
    
    def get_telemetry(self) -> Dict:
        """Get current telemetry data"""
        return {
            'speed': float(self.speed),
            'acceleration': float(self.acceleration),
            'braking_intensity': float(self.braking_intensity),
            'steering_angle': float(self.steering_angle),
            'jerk': float(self.jerk),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def send_telemetry(self, telemetry: Dict) -> Optional[Dict]:
        """Send telemetry to backend API"""
        try:
            response = requests.post(
                f"{self.api_url}/driving_data",
                json=telemetry,
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return None
    
    def run_simulation(self, duration: int = 300, update_interval: float = 1.0):
        """
        Run the driving simulation
        
        Args:
            duration: Total simulation time in seconds
            update_interval: How often to send data to backend (seconds)
        """
        print("🚗 Starting DriveMind.ai Driving Simulation")
        print(f"Duration: {duration}s, Update interval: {update_interval}s")
        print("=" * 50)
        
        start_time = time.time()
        last_update = start_time
        scenario_duration = 0
        scenario_switch_time = np.random.uniform(10, 30)
        
        # Initial scenario
        self.select_random_scenario()
        print(f"📍 Scenario: {self.scenario}")
        
        try:
            while time.time() - start_time < duration:
                current_time = time.time()
                dt = self.time_step
                
                # Switch scenario periodically
                scenario_duration += dt
                if scenario_duration > scenario_switch_time:
                    self.select_random_scenario()
                    print(f"\n📍 Scenario changed to: {self.scenario} (target: {self.target_speed:.1f} km/h)")
                    scenario_duration = 0
                    scenario_switch_time = np.random.uniform(10, 30)
                
                # Generate driving behavior
                self.generate_driving_behavior()
                
                # Update physics
                self.update_physics(dt)
                
                # Send data at specified interval
                if current_time - last_update >= update_interval:
                    telemetry = self.get_telemetry()
                    
                    # Print current state
                    print(f"🚙 Speed: {telemetry['speed']:6.1f} km/h | "
                          f"Accel: {telemetry['acceleration']:5.2f} m/s² | "
                          f"Brake: {telemetry['braking_intensity']:4.2f} | "
                          f"Steer: {telemetry['steering_angle']:5.1f}°", end='')
                    
                    # Send to backend
                    response = self.send_telemetry(telemetry)
                    
                    if response:
                        score = response.get('score', 0)
                        print(f" | Score: {score:4.1f}/10 ✅")
                    else:
                        print(" | ⚠️ No response")
                    
                    last_update = current_time
                
                # Sleep to maintain update rate
                time.sleep(dt)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Simulation interrupted by user")
        
        print("\n✅ Simulation complete!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='DriveMind.ai Driving Simulator')
    parser.add_argument('--duration', type=int, default=300, help='Simulation duration in seconds (default: 300)')
    parser.add_argument('--interval', type=float, default=1.0, help='Data update interval in seconds (default: 1.0)')
    parser.add_argument('--api-url', type=str, default='http://localhost:8000/api', help='Backend API URL')
    
    args = parser.parse_args()
    
    simulator = DrivingSimulator(api_url=args.api_url)
    simulator.run_simulation(duration=args.duration, update_interval=args.interval)

if __name__ == '__main__':
    main()
