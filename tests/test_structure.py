#!/usr/bin/env python3
"""
Test script to verify DriveMind.ai project structure and files
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} NOT FOUND")
        return False

def main():
    print("🚗 DriveMind.ai Project Structure Verification")
    print("=" * 60)
    
    base_dir = "/home/runner/work/Auralis.ai/Auralis.ai"
    os.chdir(base_dir)
    
    checks = [
        # Frontend
        ("frontend/package.json", "Frontend package.json"),
        ("frontend/vite.config.js", "Vite configuration"),
        ("frontend/tailwind.config.js", "TailwindCSS config"),
        ("frontend/src/App.jsx", "Main App component"),
        ("frontend/src/components/Dashboard.jsx", "Dashboard component"),
        ("frontend/src/components/Header.jsx", "Header component"),
        ("frontend/src/components/ScoreDisplay.jsx", "Score display"),
        ("frontend/src/components/TelemetryCharts.jsx", "Charts component"),
        ("frontend/src/hooks/useWebSocket.js", "WebSocket hook"),
        ("frontend/src/hooks/useDarkMode.js", "Dark mode hook"),
        
        # Backend
        ("backend/main.py", "Backend main application"),
        ("backend/app/routes.py", "API routes"),
        ("backend/models/schemas.py", "Pydantic schemas"),
        ("backend/services/ml_service.py", "ML service"),
        ("backend/services/supabase_service.py", "Supabase service"),
        ("backend/requirements.txt", "Backend requirements"),
        ("backend/.env.example", "Environment example"),
        
        # ML Model
        ("ml_model/generate_data.py", "Data generation script"),
        ("ml_model/train_model.py", "Model training script"),
        ("ml_model/requirements.txt", "ML requirements"),
        
        # Simulation
        ("simulation/drive_simulator.py", "Driving simulator"),
        ("simulation/requirements.txt", "Simulation requirements"),
        
        # Documentation
        ("README.md", "Main README"),
        ("LICENSE", "License file"),
        ("docs/QUICKSTART.md", "Quick start guide"),
        ("docs/ARCHITECTURE.md", "Architecture documentation"),
        ("docs/DEVELOPMENT.md", "Development guide"),
        ("docs/FAQ.md", "FAQ documentation"),
        ("docs/database_schema.md", "Database schema"),
        ("docs/api_example.py", "API usage example"),
        
        # Scripts
        ("scripts/setup.sh", "Setup script"),
        (".gitignore", "Git ignore file"),
    ]
    
    passed = 0
    failed = 0
    
    for filepath, description in checks:
        if check_file_exists(filepath, description):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All files present!")
        return 0
    else:
        print("❌ Some files are missing")
        return 1

if __name__ == "__main__":
    sys.exit(main())
