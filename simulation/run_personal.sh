#!/bin/bash
# Run personal mode simulation
# Usage: ./run_personal.sh [duration] [interval]

DURATION=${1:-300}
INTERVAL=${2:-1.0}

echo "Starting Personal Mode Simulation"
echo "Duration: ${DURATION}s, Interval: ${INTERVAL}s"
echo ""

python drive_simulator.py --duration "$DURATION" --interval "$INTERVAL" --mode personal
