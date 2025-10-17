#!/bin/bash

# DriveMind.ai Setup Script
# This script sets up all components of the project

echo "🚗 DriveMind.ai - Setup Script"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}✅ Running on macOS${NC}"
    IS_MACOS=true
else
    echo -e "${YELLOW}⚠️  Not running on macOS - some features may differ${NC}"
    IS_MACOS=false
fi

# 1. Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend
if [ -f "package.json" ]; then
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
    else
        echo -e "${RED}❌ Failed to install frontend dependencies${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ package.json not found${NC}"
    exit 1
fi
cd ..

# 2. Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install backend dependencies${NC}"
    exit 1
fi

# Setup .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Created .env file from .env.example${NC}"
    echo -e "${YELLOW}   Please update it with your Supabase credentials${NC}"
fi

cd ..

# 3. Setup ML Model
echo ""
echo "🧠 Setting up ML Model..."
cd ml_model

# Install ML dependencies
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ML dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install ML dependencies${NC}"
    exit 1
fi

# Generate training data if it doesn't exist
if [ ! -f "training_data.csv" ]; then
    echo "Generating synthetic training data..."
    python generate_data.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Training data generated${NC}"
    else
        echo -e "${RED}❌ Failed to generate training data${NC}"
        exit 1
    fi
fi

# Train model if it doesn't exist
if [ ! -f "trained_model.pkl" ]; then
    echo "Training ML model..."
    python train_model.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ ML model trained${NC}"
    else
        echo -e "${RED}❌ Failed to train ML model${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Model already exists, skipping training${NC}"
fi

cd ..

# 4. Setup Simulation
echo ""
echo "🎮 Setting up Simulation..."
cd simulation

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Simulation dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install simulation dependencies${NC}"
    exit 1
fi

cd ..

# Deactivate virtual environment
deactivate

# Final summary
echo ""
echo "================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "📝 Next Steps:"
echo "1. (Optional) Configure Supabase in backend/.env"
echo "2. (Optional) Install and run Ollama for AI feedback"
echo "3. Run the system with: ./scripts/run.sh"
echo ""
echo "Or manually:"
echo "  Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  Terminal 2: cd frontend && npm run dev"
echo "  Terminal 3: cd simulation && python drive_simulator.py"
echo ""
