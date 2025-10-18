"""
Realistic driving simulation that generates telemetry data
and sends it to the backend API in real-time using async HTTP requests
"""
import numpy as np
import asyncio
import aiohttp
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
        
        # Session tracking for independent modes
        self.session_id = None
        self.session_scores = []  # Track scores for this session
        
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
    
    def get_telemetry(self, simulation_mode: str = 'personal') -> Dict:
        """Get current telemetry data"""
        return {
            'speed': float(self.speed),
            'acceleration': float(self.acceleration),
            'braking_intensity': float(self.braking_intensity),
            'steering_angle': float(self.steering_angle),
            'jerk': float(self.jerk),
            'timestamp': datetime.utcnow().isoformat(),
            'simulation_mode': simulation_mode,
            'scenario': self.scenario
        }
    
    async def send_telemetry(self, telemetry: Dict, max_retries: int = 3) -> Optional[Dict]:
        """
        Send telemetry to backend API with retry mechanism (async version)
        
        Args:
            telemetry: Telemetry data to send
            max_retries: Maximum number of retry attempts (default: 3)
            
        Returns:
            Optional[Dict]: Response from backend or None if failed
        """
        retry_delays = [0.5, 1.0, 2.0]  # Exponential backoff delays
        
        timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for attempt in range(max_retries):
                try:
                    async with session.post(
                        f"{self.api_url}/driving_data",
                        json=telemetry
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status == 503:
                            # Backend is busy, retry
                            if attempt < max_retries - 1:
                                delay = retry_delays[attempt]
                                print(f"⏳ Backend busy, retrying in {delay}s (attempt {attempt + 1}/{max_retries})...")
                                await asyncio.sleep(delay)
                                continue
                            else:
                                print(f"❌ Backend busy after {max_retries} attempts")
                                return None
                        else:
                            error_text = await response.text()
                            print(f"❌ Error: {response.status} - {error_text}")
                            return None
                        
                except asyncio.TimeoutError:
                    if attempt < max_retries - 1:
                        delay = retry_delays[attempt]
                        print(f"⏳ Request timeout, retrying in {delay}s (attempt {attempt + 1}/{max_retries})...")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        print(f"❌ Request timeout after {max_retries} attempts")
                        return None
                        
                except aiohttp.ClientError as e:
                    if attempt < max_retries - 1:
                        delay = retry_delays[attempt]
                        print(f"⏳ Connection error: {e}, retrying in {delay}s (attempt {attempt + 1}/{max_retries})...")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        print(f"❌ Connection error after {max_retries} attempts: {e}")
                        return None
                except Exception as e:
                    if attempt < max_retries - 1:
                        delay = retry_delays[attempt]
                        print(f"⏳ Unexpected error: {e}, retrying in {delay}s (attempt {attempt + 1}/{max_retries})...")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        print(f"❌ Unexpected error after {max_retries} attempts: {e}")
                        return None
        
        return None
    
    async def run_simulation(self, duration: int = 300, update_interval: float = 1.0, 
                       simulation_mode: str = 'personal'):
        """
        Run the driving simulation (async version)
        
        Args:
            duration: Total simulation time in seconds
            update_interval: How often to send data to backend (seconds)
            simulation_mode: Simulation mode - 'personal' or 'fleet'
        """
        import uuid
        
        # Generate unique session ID for this simulation run
        self.session_id = str(uuid.uuid4())
        self.session_scores = []
        
        mode_emoji = "🚗" if simulation_mode == 'personal' else "🚕"
        print(f"{mode_emoji} Starting DriveMind.ai Driving Simulation ({simulation_mode.upper()} mode)")
        print(f"Session ID: {self.session_id}")
        print(f"Duration: {duration}s, Update interval: {update_interval}s")
        print("=" * 50)
        
        start_time = asyncio.get_event_loop().time()
        last_update = start_time
        scenario_duration = 0
        scenario_switch_time = np.random.uniform(10, 30)
        
        # Initial scenario
        self.select_random_scenario()
        print(f"📍 Scenario: {self.scenario}")
        
        try:
            while asyncio.get_event_loop().time() - start_time < duration:
                current_time = asyncio.get_event_loop().time()
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
                    telemetry = self.get_telemetry(simulation_mode)
                    telemetry['session_id'] = self.session_id
                    
                    # Print current state
                    print(f"{mode_emoji} [{simulation_mode.upper()}] Speed: {telemetry['speed']:6.1f} km/h | "
                          f"Accel: {telemetry['acceleration']:5.2f} m/s² | "
                          f"Brake: {telemetry['braking_intensity']:4.2f} | "
                          f"Steer: {telemetry['steering_angle']:5.1f}° | "
                          f"Scenario: {telemetry['scenario']:10s}", end='')
                    
                    # Send to backend with retry (async)
                    response = await self.send_telemetry(telemetry)
                    
                    if response:
                        score = response.get('score', 0)
                        self.session_scores.append(score)
                        avg_score = sum(self.session_scores) / len(self.session_scores)
                        print(f" | Score: {score:4.1f}/10 | Avg: {avg_score:4.1f}/10 ✅")
                    else:
                        print(" | ⚠️ No response")
                    
                    last_update = current_time
                
                # Sleep to maintain update rate (async)
                await asyncio.sleep(dt)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Simulation interrupted by user")
        
        # Print session summary
        print(f"\n{'='*50}")
        print(f"✅ {simulation_mode.upper()} Simulation complete!")
        print(f"Session ID: {self.session_id}")
        if self.session_scores:
            print(f"Total updates: {len(self.session_scores)}")
            print(f"Average score: {sum(self.session_scores) / len(self.session_scores):.2f}/10")
            print(f"Best score: {max(self.session_scores):.2f}/10")
            print(f"Worst score: {min(self.session_scores):.2f}/10")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='DriveMind.ai Driving Simulator')
    parser.add_argument('--duration', type=int, default=300, help='Simulation duration in seconds (default: 300)')
    parser.add_argument('--interval', type=float, default=1.0, help='Data update interval in seconds (default: 1.0)')
    parser.add_argument('--api-url', type=str, default='http://localhost:8000/api', help='Backend API URL')
    parser.add_argument('--mode', type=str, choices=['personal', 'fleet'], default='personal',
                        help='Simulation mode: personal (default) or fleet')
    
    args = parser.parse_args()
    
    simulator = DrivingSimulator(api_url=args.api_url)
    await simulator.run_simulation(duration=args.duration, update_interval=args.interval, 
                           simulation_mode=args.mode)

if __name__ == '__main__':
    asyncio.run(main())
