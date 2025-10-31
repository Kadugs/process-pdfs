# Process PDFs

A small ETL pipeline that extracts structured information from PDF files.

## Overview

This repository contains extractors, transformers and loaders to process PDFs and
produce structured data. Key features:

- PDF extraction using `pdfplumber`.
- Per-document mapping and standardization (JSON mappings + optional JSON Schema).
- Export of cleaned data to Parquet and SQL dump files (ready for PostgreSQL).
- Interactive file selection in terminal using `inquirer`.

## Quick start

1. Run the installer (creates a virtualenv and installs dependencies):

```bash
./install.sh
```

2. Activate the virtual environment (if not already active):

```bash
source venv/bin/activate
```

3. Run the application (interactive selection):

```bash
./run.sh
```

Or run directly:

```bash
python -m src.main
```

## What the application does

- Scans `data/input/` for PDF files and lets you choose one to process.
- Routes the PDF to the correct extractor (e.g. `specifications_for_constructions`,
  `sample_invoice`). Extractors return a pandas DataFrame.
- Standardizes the DataFrame using a mapping JSON found in
  `src/transform/configs/<document_type>.json`. If a sibling
  `*.schema.json` exists the mapping is validated before use.
- Saves standardized data to `data/<document_type>_df.parquet`.
- Exports an SQL dump to `tmp/<document_type>.sql` with CREATE TABLE and batched
  INSERT statements (suitable for loading into PostgreSQL).

## Adding or updating mappings

Mappings live in `src/transform/configs/` and are simple JSON objects with a
`mapping` key that maps canonical target fields to source column names (or
`null` to create an empty column). Example:

```json
{
  "document_id": 1,
  "mapping": {
    "item_description": "Service Description",
    "price": "Amount -without VAT-",
    "quantity": "quantity",
    "invoice_number": "Invoice No",
    "customer_number": "Customer No",
    "contractor": "Service Contractor",
    "client_name": "Client Name",
    "tax_rate": "VAT Percentage",
    "item_code": null,
    "details": null
  }
}
```

If a schema file with the same name and `.schema.json` suffix exists it will be
used to validate the mapping before standardization. See
`src/transform/configs/*.schema.json` for examples.

## SQL dump and loading into PostgreSQL

After standardization the pipeline writes an SQL dump to `data/output/extracted_documents.sql`.
The dump includes a `CREATE TABLE` followed by batched `INSERT` statements.
To load the dump into PostgreSQL locally:

```bash
psql -d your_database -f data/output/extracted_documents.sql
```

## Development

Install development dependencies:

```bash
sh install.sh
```

or

```bash
pip install -r requirements-dev.txt
```

## Dependencies

Main runtime dependencies are listed in `requirements.txt` and include:

- pdfplumber
- pandas
- matplotlib
- inquirer (interactive file selection)

Dev dependencies and tooling may be configured in `pyproject.toml` (if present).

## Project layout

- `src/extract/` — extractor modules per document type
- `src/transform/` — standardization and mapping logic
- `src/load/` — CSV/SQL dump helpers
- `data/` — input PDFs and generated files

## Author

Carlos Eduardo Gomes Silva
