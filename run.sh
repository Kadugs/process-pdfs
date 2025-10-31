#!/bin/bash

if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run install.sh first."
    exit 1
fi

echo "Running..."
python src/main.py
