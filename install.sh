#!/bin/bash

echo "Installing Process PDFs dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the project in editable mode so imports work (no per-file sys.path hacks required)
echo "Installing project in editable mode..."
pip install -e .

# Also install extra requirements if present
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
fi

echo ""
echo "Installation completed"
echo ""
echo "To use the project:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the script: python main.py"
echo ""
echo "Or use the runner script: ./run.sh"
