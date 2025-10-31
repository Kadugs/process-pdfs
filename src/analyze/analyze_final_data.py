import pandas as pd
from pathlib import Path


def generate_analysis(file_path: str):
    df = pd.read_csv(file_path)
    number_of_documents = df["document_id"].nunique()
    print(f"Number of unique documents: {number_of_documents}")
    number_of_items = df.shape[0]
    total_price = df[["price", "quantity"]].prod(axis=1).sum()

    project_root = Path(__file__).resolve().parents[2]
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    md_path = reports_dir / "analysis_summary.md"
    percentage_of_lines_with_details = (
        df["details"].notna().sum() / number_of_items
    ) * 100
    md_content = f"""# Analysis Summary (generated)

This report contains the basic metrics produced by `generate_analysis()` in
`src/analyze/analyze_final_data.py`. It uses only the three metrics the
current analysis computes.

---

## Number of unique documents

Description: Count of distinct `document_id` values in the extracted data.

Value: {number_of_documents}

---

## Number of item lines

Description: Total number of rows (item lines) in the extracted dataset.

Value: {number_of_items}

---

## Total price (sum of price * quantity)

Description: Sum of `price * quantity` computed per row and then aggregated.

Value: {total_price:.2f}

---

## Percentage of lines with details
Description: Percentage of item lines that have non-empty `details` field.

Value: {percentage_of_lines_with_details:.2f}%


"""

    md_path.write_text(md_content, encoding="utf-8")
    print(f"Markdown saved to: {md_path}")
