"""
Process PDFs - A small ETL pipeline that extracts structured information
  from PDF files.

This package provides tools and utilities for processing
  PDF documents and extracting
structured data from them using pdfplumber, pandas, and matplotlib.
"""

__version__ = "0.1.0"
__author__ = "Carlos Eduardo Gomes Silva"
__email__ = "66494905+Kadugs@users.noreply.github.com"

from . import extract, transform, load

__all__ = ["extract", "transform", "load"]
