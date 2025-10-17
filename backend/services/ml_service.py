import os
import pickle
import numpy as np
from typing import Optional
from datetime import datetime
from models.schemas import DrivingData
import requests
from dotenv import load_dotenv

load_dotenv()

class MLService:
    """
    Machine Learning service for calculating driving safety scores
    """
    
    def __init__(self):
        self.model = None
        self.last_score = None
        self.ollama_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
        
        # Determine model path - handle both relative and absolute paths
        # __file__ is in backend/services/ml_service.py, so we need to go up to project root
        default_model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'ml_model', 'trained_model.pkl'
        ))
        self.model_path = os.getenv('MODEL_PATH', default_model_path)
        
        # Try to load the trained model
        self._load_model()
    
    def _load_model(self):
        """Load the trained ML model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    loaded_data = pickle.load(f)
                
                # Handle both dictionary format (from train_model.py) and direct model format
                if isinstance(loaded_data, dict):
                    # Dictionary format with 'model' key
                    if 'model' in loaded_data:
                        self.model = loaded_data['model']
                        print(f"✅ ML model loaded from {self.model_path} (type: {loaded_data.get('type', 'unknown')})")
                    else:
                        print(f"⚠️ Invalid model format in {self.model_path}. Using rule-based scoring.")
                else:
                    # Direct model object
                    self.model = loaded_data
                    print(f"✅ ML model loaded from {self.model_path}")
            else:
                print(f"⚠️ Model file not found at {self.model_path}. Using rule-based scoring.")
        except Exception as e:
            print(f"❌ Error loading model: {e}. Using rule-based scoring.")
    
    def calculate_score(self, data: DrivingData) -> float:
        """
        Calculate driving safety score from telemetry data
        
        Args:
            data: DrivingData object containing telemetry
            
        Returns:
            float: Safety score between 0 and 10
        """
        if self.model is not None:
            # Use ML model for prediction
            try:
                features = self._extract_features(data)
                score = self.model.predict([features])[0]
                # Ensure score is within bounds
                score = max(0.0, min(10.0, score))
            except Exception as e:
                print(f"Error using ML model: {e}. Falling back to rule-based.")
                score = self._rule_based_score(data)
        else:
            # Use rule-based scoring
            score = self._rule_based_score(data)
        
        self.last_score = score
        return score
    
    def _extract_features(self, data: DrivingData) -> list:
        """Extract features for ML model"""
        return [
            data.speed,
            data.acceleration,
            data.braking_intensity,
            abs(data.steering_angle),
            data.jerk if data.jerk is not None else 0.0,
        ]
    
    def _rule_based_score(self, data: DrivingData) -> float:
        """
        Calculate score using rule-based approach
        
        Scoring factors:
        - Speed: penalty for excessive speed
        - Acceleration: penalty for harsh acceleration
        - Braking: penalty for harsh braking
        - Steering: penalty for sharp steering
        - Jerk: penalty for sudden changes
        """
        score = 10.0  # Start with perfect score
        
        # Speed penalty (assuming speed limit of 80 km/h for simulation)
        if data.speed > 100:
            score -= 2.0
        elif data.speed > 80:
            score -= 1.0
        
        # Acceleration penalty
        if abs(data.acceleration) > 3.0:
            score -= 1.5
        elif abs(data.acceleration) > 2.0:
            score -= 0.8
        
        # Braking penalty
        if data.braking_intensity > 0.7:
            score -= 1.5
        elif data.braking_intensity > 0.4:
            score -= 0.8
        
        # Steering penalty
        if abs(data.steering_angle) > 30:
            score -= 1.0
        elif abs(data.steering_angle) > 15:
            score -= 0.5
        
        # Jerk penalty (if available)
        if data.jerk is not None:
            if abs(data.jerk) > 2.0:
                score -= 0.5
        
        # Ensure score is within bounds
        return max(0.0, min(10.0, score))
    
    def get_last_score(self) -> Optional[float]:
        """Get the last calculated score"""
        return self.last_score
    
    async def generate_feedback(self, score: float, data: DrivingData) -> str:
        """
        Generate AI feedback using Ollama LLM (if available) or rule-based feedback
        
        Args:
            score: Current driving score
            data: Current driving data
            
        Returns:
            str: Feedback message
        """
        # Try to use Ollama for AI-generated feedback
        try:
            feedback = await self._generate_ollama_feedback(score, data)
            if feedback:
                return feedback
        except Exception as e:
            print(f"Ollama not available: {e}")
        
        # Fall back to rule-based feedback
        return self._generate_rule_based_feedback(score, data)
    
    async def _generate_ollama_feedback(self, score: float, data: DrivingData) -> Optional[str]:
        """Generate feedback using Ollama LLM"""
        try:
            prompt = f"""You are a professional driving instructor analyzing driving behavior.

Current Driving Metrics:
- Safety Score: {score:.1f}/10
- Speed: {data.speed:.1f} km/h
- Acceleration: {data.acceleration:.2f} m/s²
- Braking Intensity: {data.braking_intensity:.2f}
- Steering Angle: {data.steering_angle:.1f}°

Provide brief, constructive feedback (2-3 sentences) to help improve driving safety. Be encouraging but specific about areas of concern."""

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
        except Exception as e:
            print(f"Ollama generation error: {e}")
        
        return None
    
    def _generate_rule_based_feedback(self, score: float, data: DrivingData) -> str:
        """Generate rule-based feedback"""
        feedback_parts = []
        
        if score >= 8:
            feedback_parts.append("Excellent driving! You're maintaining good control and safe practices.")
        elif score >= 6:
            feedback_parts.append("Good driving overall, but there's room for improvement.")
        elif score >= 4:
            feedback_parts.append("Your driving shows some concerning patterns that need attention.")
        else:
            feedback_parts.append("Please focus on safer driving practices.")
        
        # Specific feedback based on metrics
        if data.speed > 80:
            feedback_parts.append("Consider reducing your speed for safer driving.")
        
        if abs(data.acceleration) > 2.0:
            feedback_parts.append("Try to accelerate more smoothly to improve fuel efficiency and safety.")
        
        if data.braking_intensity > 0.5:
            feedback_parts.append("Gentle braking improves safety and reduces wear on your vehicle.")
        
        if abs(data.steering_angle) > 20:
            feedback_parts.append("Smoother steering inputs provide better vehicle control.")
        
        return " ".join(feedback_parts)
    
    async def generate_driver_feedback(self, driver_stats: dict) -> str:
        """
        Generate AI feedback for a driver based on their aggregate stats
        
        Args:
            driver_stats: Dictionary containing driver statistics (avg_score, avg_speed, etc.)
            
        Returns:
            str: Feedback message for the driver
        """
        avg_score = driver_stats.get('avg_score', 0)
        trip_count = driver_stats.get('trip_count', 0)
        avg_speed = driver_stats.get('avg_speed', 0)
        avg_braking = driver_stats.get('avg_braking', 0)
        
        # Try to use Ollama for AI-generated feedback
        try:
            feedback = await self._generate_ollama_driver_feedback(driver_stats)
            if feedback:
                return feedback
        except Exception as e:
            print(f"Ollama not available for driver feedback: {e}")
        
        # Fall back to rule-based feedback
        feedback_parts = []
        
        if avg_score >= 8:
            feedback_parts.append(f"Outstanding performance! Maintaining an average score of {avg_score:.1f}/10 over {trip_count} trips.")
        elif avg_score >= 6:
            feedback_parts.append(f"Good driving record with {avg_score:.1f}/10 average. Focus on consistency.")
        elif avg_score >= 4:
            feedback_parts.append(f"Average score of {avg_score:.1f}/10 needs improvement. Review your driving habits.")
        else:
            feedback_parts.append(f"Score of {avg_score:.1f}/10 is concerning. Immediate attention needed.")
        
        # Speed feedback
        if avg_speed > 70:
            feedback_parts.append("Reduce average speed for better safety scores.")
        elif avg_speed < 40:
            feedback_parts.append("Good speed control maintained.")
        
        # Braking feedback
        if avg_braking > 0.5:
            feedback_parts.append("Heavy braking detected. Try anticipating stops earlier.")
        else:
            feedback_parts.append("Smooth braking patterns observed.")
        
        return " ".join(feedback_parts)
    
    async def _generate_ollama_driver_feedback(self, driver_stats: dict) -> Optional[str]:
        """Generate feedback for a driver using Ollama LLM"""
        try:
            avg_score = driver_stats.get('avg_score', 0)
            trip_count = driver_stats.get('trip_count', 0)
            avg_speed = driver_stats.get('avg_speed', 0)
            avg_acceleration = driver_stats.get('avg_acceleration', 0)
            avg_braking = driver_stats.get('avg_braking', 0)
            
            prompt = f"""You are a professional fleet manager analyzing driver performance.

Driver Statistics:
- Average Safety Score: {avg_score:.1f}/10
- Total Trips: {trip_count}
- Average Speed: {avg_speed:.1f} km/h
- Average Acceleration: {avg_acceleration:.2f} m/s²
- Average Braking Intensity: {avg_braking:.2f}

Provide brief, actionable feedback (1-2 sentences) to help this driver improve. Be professional and constructive."""

            # Try mistral:7b-instruct-q4_0 first, then fall back to mistral:latest
            models_to_try = ["mistral:7b-instruct-q4_0", "mistral:latest", "mistral"]
            
            for model in models_to_try:
                try:
                    response = requests.post(
                        f"{self.ollama_url}/api/generate",
                        json={
                            "model": model,
                            "prompt": prompt,
                            "stream": False
                        },
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        feedback = result.get('response', '').strip()
                        if feedback:
                            print(f"✅ Generated driver feedback using model: {model}")
                            return feedback
                except Exception as model_error:
                    print(f"Failed to use model {model}: {model_error}")
                    continue
            
        except Exception as e:
            print(f"Ollama driver feedback generation error: {e}")
        
        return None
    
    async def generate_fleet_insights(self, fleet_summary: dict, driver_stats: list) -> str:
        """
        Generate fleet-level insights using AI
        
        Args:
            fleet_summary: Fleet-level statistics
            driver_stats: List of individual driver statistics
            
        Returns:
            str: Fleet insights message
        """
        # Try to use Ollama for AI-generated insights
        try:
            insights = await self._generate_ollama_fleet_insights(fleet_summary, driver_stats)
            if insights:
                return insights
        except Exception as e:
            print(f"Ollama not available for fleet insights: {e}")
        
        # Fall back to rule-based insights
        total_drivers = fleet_summary.get('total_drivers', 0)
        fleet_avg = fleet_summary.get('fleet_avg_score', 0)
        safest_driver = fleet_summary.get('safest_driver', 'N/A')
        
        # Find most improved driver (simplified - would need historical data)
        sorted_drivers = sorted(driver_stats, key=lambda x: x.get('avg_score', 0), reverse=True)
        
        insights_parts = []
        insights_parts.append(f"Fleet Overview: {total_drivers} drivers with {fleet_avg:.1f}/10 average score.")
        insights_parts.append(f"Top Performer: {safest_driver}.")
        
        if fleet_avg >= 7:
            insights_parts.append("Overall fleet performance is strong. Maintain current standards.")
        elif fleet_avg >= 5:
            insights_parts.append("Fleet performance is acceptable but has room for improvement.")
        else:
            insights_parts.append("Fleet performance requires immediate attention and training.")
        
        # Identify drivers needing attention
        low_scorers = [d for d in driver_stats if d.get('avg_score', 0) < 5]
        if low_scorers:
            insights_parts.append(f"{len(low_scorers)} driver(s) need additional training and support.")
        
        return " ".join(insights_parts)
    
    async def _generate_ollama_fleet_insights(self, fleet_summary: dict, driver_stats: list) -> Optional[str]:
        """Generate fleet insights using Ollama LLM"""
        try:
            total_drivers = fleet_summary.get('total_drivers', 0)
            fleet_avg = fleet_summary.get('fleet_avg_score', 0)
            total_trips = fleet_summary.get('total_trips', 0)
            
            # Calculate additional metrics
            high_performers = len([d for d in driver_stats if d.get('avg_score', 0) >= 8])
            low_performers = len([d for d in driver_stats if d.get('avg_score', 0) < 5])
            
            prompt = f"""You are a fleet operations analyst providing insights to management.

Fleet Metrics:
- Total Drivers: {total_drivers}
- Total Trips: {total_trips}
- Average Fleet Score: {fleet_avg:.1f}/10
- High Performers (8+): {high_performers}
- Low Performers (<5): {low_performers}

Provide brief, actionable insights (2-3 sentences) for fleet management. Focus on trends and recommendations."""

            # Try mistral:7b-instruct-q4_0 first, then fall back to mistral:latest
            models_to_try = ["mistral:7b-instruct-q4_0", "mistral:latest", "mistral"]
            
            for model in models_to_try:
                try:
                    response = requests.post(
                        f"{self.ollama_url}/api/generate",
                        json={
                            "model": model,
                            "prompt": prompt,
                            "stream": False
                        },
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        insights = result.get('response', '').strip()
                        if insights:
                            print(f"✅ Generated fleet insights using model: {model}")
                            return insights
                except Exception as model_error:
                    print(f"Failed to use model {model}: {model_error}")
                    continue
            
        except Exception as e:
            print(f"Ollama fleet insights generation error: {e}")
        
        return None
