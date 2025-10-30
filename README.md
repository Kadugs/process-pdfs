# Process PDFs

A small ETL pipeline that extracts structured information from PDF files.

## Description

This project provides tools and utilities for processing PDF documents and extracting structured data from them.

## Installation

### Using Poetry (Recommended)

Install dependencies using Poetry:

```bash
poetry install
```

Or use the Makefile:

```bash
make install
```

### Using pip and setup.py

You can also install the package in development mode:

```bash
# Install package in development mode
make install-dev

# Or with development dependencies
make install-dev-extras

# Or directly with pip
pip install -e .
pip install -e ".[dev]"  # with dev dependencies
```

## Usage

This project includes a Makefile with convenient commands:

```bash
# Show all available commands
make help

# Install dependencies
make install

# Update dependencies
make update

# Process PDFs in the input directory
make process-pdfs

# Run the main script
make run

# Clean up temporary files
make clean

# Install package in development mode
make install-dev

# Build distribution packages
make build

# Check setup.py configuration
make check-setup
```

### Processing PDFs

Place your PDF files in the `data/input/` directory and run:

```bash
make process-pdfs
```

Or run the main script directly:

```bash
make run
```

## Dependencies

- pdfplumber: For PDF text extraction
- matplotlib: For data visualization
- pandas: For data manipulation

## Author

Carlos Eduardo Gomes Silva
