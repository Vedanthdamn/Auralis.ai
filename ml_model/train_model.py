"""
Train ML model for driver safety scoring
Supports both scikit-learn and TensorFlow models
Optimized for macOS Apple Silicon (M1/M2/M4)
"""
import os
import sys
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

# TensorFlow for Apple Silicon
try:
    import tensorflow as tf
    # Enable Metal acceleration on macOS
    if sys.platform == 'darwin':
        print("🍎 Running on macOS - Metal acceleration enabled")
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("⚠️ TensorFlow not installed. Using scikit-learn models only.")
    TENSORFLOW_AVAILABLE = False

def load_data(filepath: str = 'training_data.csv'):
    """Load training data from CSV"""
    if not os.path.exists(filepath):
        print(f"❌ Data file not found: {filepath}")
        print("Run generate_data.py first to create training data.")
        sys.exit(1)
    
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} samples from {filepath}")
    
    # Features and target
    feature_columns = ['speed', 'acceleration', 'braking_intensity', 'steering_angle', 'jerk']
    X = df[feature_columns].values
    y = df['safety_score'].values
    
    return X, y, feature_columns

def train_sklearn_model(X_train, y_train, X_test, y_test, model_type='random_forest'):
    """Train scikit-learn model"""
    print(f"\n🔧 Training {model_type} model...")
    
    if model_type == 'random_forest':
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
    elif model_type == 'gradient_boosting':
        model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train
    model.fit(X_train, y_train)
    
    # Evaluate
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    
    print(f"\n📊 {model_type.replace('_', ' ').title()} Results:")
    print(f"Train RMSE: {train_rmse:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")
    print(f"Test MAE: {test_mae:.4f}")
    print(f"Train R²: {train_r2:.4f}")
    print(f"Test R²: {test_r2:.4f}")
    
    return model, test_r2

def train_tensorflow_model(X_train, y_train, X_test, y_test, scaler):
    """Train TensorFlow neural network model (optimized for Apple Silicon)"""
    if not TENSORFLOW_AVAILABLE:
        return None, 0.0
    
    print("\n🧠 Training TensorFlow Neural Network...")
    
    # Scale data for neural network
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    
    # Compile with Adam optimizer
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='mse',
        metrics=['mae']
    )
    
    # Early stopping
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )
    
    # Train
    history = model.fit(
        X_train_scaled, y_train,
        validation_data=(X_test_scaled, y_test),
        epochs=100,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=0
    )
    
    # Evaluate
    train_pred = model.predict(X_train_scaled, verbose=0).flatten()
    test_pred = model.predict(X_test_scaled, verbose=0).flatten()
    
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    
    print(f"\n📊 TensorFlow NN Results:")
    print(f"Train RMSE: {train_rmse:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")
    print(f"Test MAE: {test_mae:.4f}")
    print(f"Train R²: {train_r2:.4f}")
    print(f"Test R²: {test_r2:.4f}")
    print(f"Training epochs: {len(history.history['loss'])}")
    
    return model, test_r2

def main():
    print("🚗 DriveMind.ai - ML Model Training")
    print("=" * 50)
    
    # Load data
    X, y, feature_columns = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\n📊 Data split:")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features: {feature_columns}")
    
    # Scale data
    scaler = StandardScaler()
    scaler.fit(X_train)
    
    # Train multiple models and select the best
    models = {}
    scores = {}
    
    # Train Random Forest
    rf_model, rf_score = train_sklearn_model(X_train, y_train, X_test, y_test, 'random_forest')
    models['random_forest'] = rf_model
    scores['random_forest'] = rf_score
    
    # Train Gradient Boosting
    gb_model, gb_score = train_sklearn_model(X_train, y_train, X_test, y_test, 'gradient_boosting')
    models['gradient_boosting'] = gb_model
    scores['gradient_boosting'] = gb_score
    
    # Train TensorFlow model (if available)
    if TENSORFLOW_AVAILABLE:
        tf_model, tf_score = train_tensorflow_model(X_train, y_train, X_test, y_test, scaler)
        models['tensorflow'] = tf_model
        scores['tensorflow'] = tf_score
    
    # Select best model
    best_model_name = max(scores, key=scores.get)
    best_model = models[best_model_name]
    best_score = scores[best_model_name]
    
    print(f"\n🏆 Best model: {best_model_name} (R² = {best_score:.4f})")
    
    # Save the best model
    if best_model_name == 'tensorflow':
        # Save TensorFlow model
        best_model.save('trained_model_tf')
        # Also save scaler
        joblib.dump(scaler, 'scaler.pkl')
        print("✅ TensorFlow model saved to 'trained_model_tf/'")
        print("✅ Scaler saved to 'scaler.pkl'")
        
        # Create a wrapper for easy loading
        wrapper = {
            'type': 'tensorflow',
            'model_path': 'trained_model_tf',
            'scaler': scaler,
            'feature_columns': feature_columns
        }
        with open('trained_model.pkl', 'wb') as f:
            pickle.dump(wrapper, f)
    else:
        # Save scikit-learn model
        model_data = {
            'model': best_model,
            'scaler': scaler,
            'feature_columns': feature_columns,
            'type': best_model_name
        }
        with open('trained_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        print("✅ Model saved to 'trained_model.pkl'")
    
    print("\n✅ Training complete!")
    print(f"Model ready for inference with R² score: {best_score:.4f}")

if __name__ == '__main__':
    main()
