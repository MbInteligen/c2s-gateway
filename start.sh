#!/bin/bash
# C2S Gateway Startup Script

echo "=========================================="
echo "Starting C2S Gateway"
echo "=========================================="

# Activate virtual environment
source venv/bin/activate

# Start the gateway
python main.py
