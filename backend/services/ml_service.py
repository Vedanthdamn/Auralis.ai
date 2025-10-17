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
        # __file__ is in backend/services/ml_service.py, so we need to go up 2 levels
        default_model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'ml_model', 
            'trained_model.pkl'
        )
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
