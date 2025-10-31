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

4. Select the option that corresponds to the PDF you want to process. If you want to proccess all PDFs in the input folder, select "Process all files". It will generate standardized csv, parquet and SQL dump files in the `data/output/` folder.

## What the application does

- Scans `data/input/` for PDF files and lets you choose one to process.
- Routes the PDF to the correct extractor (e.g. `specifications_for_constructions`,
  `sample_invoice`). Extractors return a pandas DataFrame.
- Standardizes the DataFrame using a mapping JSON found in
  `src/transform/configs/<document_type>.json`.
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

## SQL dump and loading into PostgreSQL

After standardization the pipeline writes an SQL dump to `data/output/extracted_documents.sql`.
The dump includes a `CREATE TABLE` followed by batched `INSERT` statements.
To load the dump into PostgreSQL locally:

```bash
psql -d your_database -f data/output/extracted_documents.sql
```

## Semantic mapping decisions

This project maps heterogeneous extractor outputs to a single canonical schema to make downstream processing consistent. Below are the key decisions and conventions used by the standardizer (`src/transform/standardize_data.py`) and the mapping JSONs in `src/transform/configs/`.

Canonical fields (examples)

- item_description: string — free-text describing the row/section/item
- price: numeric — price or amount (stored as number when possible)
- quantity: numeric — quantity or count
- invoice_number: string
- customer_number: string
- contractor: string — party responsible for delivering the work
- client_name: string
- tax_rate: numeric or string — percentage; mappings should indicate percent values
- item_code: string — unique code or section number
- details: string — auxiliary free-text, on the sample invoice, for example, is the value of the pages of each section
- document_description: string — higher level document title

Mapping decisions (current configs)

- `specifications_for_constructions`:

  - `section_name` -> `item_description`
  - `section_code` -> `item_code`
  - `title` -> `document_description`
  - `author` -> `contractor`
  - `description` -> `details`
  - numeric/amount fields: not present; leave `price`/`quantity` null

- `sample_invoice`:
  - `Service Description` -> `item_description`
  - `Amount -without VAT-` -> `price`
  - `quantity` -> `quantity`
  - `Invoice No` -> `invoice_number`
  - `Customer No` -> `customer_number`
  - `Service Contractor` -> `contractor`
  - `Client Name` -> `client_name`
  - `VAT Percentage` -> `tax_rate`

Guidelines for adding mappings

- Create `src/transform/configs/<document_type>.json` with the `mapping` structure.
- Provide source column names exactly as they appear in the extractor output (before normalization). The standardizer will normalize them when applying the mapping.

Handling semantic differences

- Documents that represent different granularities (invoices with item lines vs. specifications with sections) are mapped to the same canonical fields, but downstream consumers should be aware of the document `type` and treat `item_description` vs `section` semantics accordingly.
- When a document lacks a field (e.g., `price` in specifications), leave the canonical field present and null to preserve schema stability.
- For ambiguous fields (e.g., `tax_rate` stored as "20%"), add small transformation code in the mapping layer or post-process to normalize to a numeric value (0.2) if required by downstream systems.

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

### Reasons to use specific dependencies

- `pdfplumber`: Robust PDF text extraction with table support, which is essential for parsing tabular data from invoices and specifications.
- `pandas`: Excellent data manipulation library, ideal for handling large datasets and performing transformations.
- `inquirer`: Provides a user-friendly command-line interface for selecting files interactively, enhancing usability.

## Project layout

- `src/extract/` — extractor modules per document type
- `src/transform/` — standardization and mapping logic
- `src/load/` — CSV/SQL dump helpers
- `data/` — input PDFs and generated files

## Credit for used pdfs

- [Standard Specification for Construction of Public Infrastructure](https://clients.bolton-menk.com/)
- [Sample Invoice PDF](https://www.wmaccess.com/downloads/sample-invoice.pdf)
- [Scanned Receipt PDF](https://www.kaggle.com/datasets/jenswalter/receipts)

## Author

Carlos Eduardo Gomes Silva
