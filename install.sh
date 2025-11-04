#!/bin/bash

echo "Installing Process PDFs dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

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
