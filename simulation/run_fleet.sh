#!/bin/bash
# Run fleet mode simulation
# Usage: ./run_fleet.sh [duration] [interval]

DURATION=${1:-300}
INTERVAL=${2:-1.0}

echo "Starting Fleet Mode Simulation"
echo "Duration: ${DURATION}s, Interval: ${INTERVAL}s"
echo ""

python drive_simulator.py --duration "$DURATION" --interval "$INTERVAL" --mode fleet
