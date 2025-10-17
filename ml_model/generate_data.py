"""
Generate synthetic driving data for training the ML model
"""
import numpy as np
import pandas as pd
from typing import Tuple

def generate_driving_data(n_samples: int = 10000, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic driving telemetry data with corresponding safety scores
    
    Features:
        - speed (km/h): 0-120
        - acceleration (m/s²): -5 to 5
        - braking_intensity: 0-1
        - steering_angle (degrees): -45 to 45
        - jerk (m/s³): -3 to 3
    
    Target:
        - safety_score: 0-10 (calculated based on driving behavior)
    
    Args:
        n_samples: Number of samples to generate
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (features, scores)
    """
    np.random.seed(seed)
    
    # Generate different driving profiles
    profiles = ['safe', 'moderate', 'aggressive', 'erratic']
    profile_weights = [0.4, 0.3, 0.2, 0.1]  # More safe drivers than aggressive
    
    features = []
    scores = []
    
    for _ in range(n_samples):
        profile = np.random.choice(profiles, p=profile_weights)
        
        if profile == 'safe':
            # Safe driver: moderate speed, gentle acceleration/braking
            speed = np.random.normal(60, 10)
            acceleration = np.random.normal(0, 0.5)
            braking = np.random.beta(2, 8)  # Low braking intensity
            steering = np.random.normal(0, 5)
            jerk = np.random.normal(0, 0.3)
            base_score = 9.0
            
        elif profile == 'moderate':
            # Moderate driver: occasional quick maneuvers
            speed = np.random.normal(70, 15)
            acceleration = np.random.normal(0, 1.0)
            braking = np.random.beta(3, 5)
            steering = np.random.normal(0, 10)
            jerk = np.random.normal(0, 0.7)
            base_score = 7.0
            
        elif profile == 'aggressive':
            # Aggressive driver: high speed, harsh acceleration/braking
            speed = np.random.normal(90, 15)
            acceleration = np.random.normal(0, 2.0)
            braking = np.random.beta(5, 3)  # High braking intensity
            steering = np.random.normal(0, 15)
            jerk = np.random.normal(0, 1.5)
            base_score = 4.0
            
        else:  # erratic
            # Erratic driver: unpredictable behavior
            speed = np.random.normal(75, 25)
            acceleration = np.random.normal(0, 2.5)
            braking = np.random.beta(4, 4)
            steering = np.random.normal(0, 20)
            jerk = np.random.normal(0, 2.0)
            base_score = 3.0
        
        # Clip values to realistic ranges
        speed = np.clip(speed, 0, 120)
        acceleration = np.clip(acceleration, -5, 5)
        braking = np.clip(braking, 0, 1)
        steering = np.clip(steering, -45, 45)
        jerk = np.clip(jerk, -3, 3)
        
        # Calculate score with some noise
        score = base_score + np.random.normal(0, 0.5)
        
        # Apply penalties based on metrics
        if speed > 100:
            score -= 2.0
        elif speed > 80:
            score -= 1.0
        
        if abs(acceleration) > 3.0:
            score -= 1.5
        elif abs(acceleration) > 2.0:
            score -= 0.8
        
        if braking > 0.7:
            score -= 1.5
        elif braking > 0.4:
            score -= 0.8
        
        if abs(steering) > 30:
            score -= 1.0
        elif abs(steering) > 15:
            score -= 0.5
        
        if abs(jerk) > 2.0:
            score -= 0.5
        
        # Ensure score is in valid range
        score = np.clip(score, 0, 10)
        
        features.append([speed, acceleration, braking, abs(steering), abs(jerk)])
        scores.append(score)
    
    return np.array(features), np.array(scores)

def save_to_csv(features: np.ndarray, scores: np.ndarray, filename: str = 'training_data.csv'):
    """Save generated data to CSV file"""
    df = pd.DataFrame(
        features,
        columns=['speed', 'acceleration', 'braking_intensity', 'steering_angle', 'jerk']
    )
    df['safety_score'] = scores
    
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(df)} samples to {filename}")
    print(f"\nData statistics:")
    print(df.describe())
    
    return df

if __name__ == '__main__':
    print("🚗 Generating synthetic driving data...")
    
    # Generate training data
    X, y = generate_driving_data(n_samples=10000)
    
    # Save to CSV
    df = save_to_csv(X, y, 'training_data.csv')
    
    print(f"\n📊 Score distribution:")
    print(f"Mean: {y.mean():.2f}")
    print(f"Std: {y.std():.2f}")
    print(f"Min: {y.min():.2f}")
    print(f"Max: {y.max():.2f}")
