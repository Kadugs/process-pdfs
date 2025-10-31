# Process PDFs

A small ETL pipeline that extracts structured information from PDF files.

## Description

This project provides tools and utilities for processing PDF documents and extracting structured data from them.

## Quick Start

### 1. Installation (One-time setup)

```bash
./install.sh
```

### 2. Running the application

```bash
./run.sh
```

Or manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

## Manual Installation

If you prefer to install manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Setup (recommended)

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the project and dependencies in editable mode:

   ```bash
   pip install --upgrade pip
   pip install -e .
   ```

This makes the `src` package importable (so `from extract...` works) and lets you edit code without reinstalling.

## Alternative: PYTHONPATH

If you prefer not to install the project, set PYTHONPATH to include the `src` folder before running scripts:

```bash
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
python main.py
```

For zsh, add the export to `~/.zshrc` to make it persistent.

## Usage

### Processing PDFs

1. Place your PDF files in the `data/input/` directory
2. Run the application:
   ```bash
   ./run.sh
   ```
   Or manually:
   ```bash
   source venv/bin/activate
   python main.py
   ```

The application will automatically:

- Look for PDF files in `data/input/`
- Process the first PDF file found
- Extract and display the text content

### Development

If you want to modify the code:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Format code
black src/
isort src/

# Check code quality
flake8 src/
```

## Dependencies

- pdfplumber: For PDF text extraction
- matplotlib: For data visualization
- pandas: For data manipulation

## Author

Carlos Eduardo Gomes Silva
