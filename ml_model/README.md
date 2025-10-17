# ML Model Directory

This directory contains the machine learning model for driver safety scoring.

## Quick Start

The backend will work even without a trained model (it will use rule-based scoring). However, for better accuracy, you can train the ML model:

### Option 1: Quick Training (Recommended)

```bash
# Install dependencies
pip install numpy scikit-learn

# Train the model (generates synthetic data automatically)
python train_model.py
```

This will create `trained_model.pkl` which the backend will automatically load at startup.

### Option 2: Generate Custom Training Data

```bash
# First, generate training data
python generate_data.py

# Then train the model
python train_model.py
```

## How It Works

1. **Training Data**: The model is trained on synthetic driving data with features:
   - Speed (km/h)
   - Acceleration (m/s²)
   - Braking intensity (0-1)
   - Steering angle (degrees)
   - Jerk (m/s³)

2. **Model**: Random Forest Regressor that predicts safety scores (0-10)

3. **Fallback**: If the model file is missing, the backend automatically falls back to rule-based scoring

## Files

- `generate_data.py` - Generates synthetic training data
- `train_model.py` - Trains the Random Forest model
- `trained_model.pkl` - Trained model (excluded from git, generated locally)
- `requirements.txt` - Python dependencies for ML training

## Notes

- The `.pkl` file is excluded from git because it's a large binary file
- Each user should train their own model locally
- The backend gracefully handles missing models by using rule-based scoring
