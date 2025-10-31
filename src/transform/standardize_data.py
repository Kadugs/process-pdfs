import json
from pathlib import Path

import numpy as np
import pandas as pd
from .configs.required_columns import required_columns


def standardize_data(df: pd.DataFrame, mapping_path: str) -> pd.DataFrame:
    df = df.copy()

    if mapping_path is None:
        raise ValueError(
            "mapping_path is required (e.g. 'src/transform/configs/[name].json')"
        )

    mapping_file = Path(mapping_path)
    if not mapping_file.exists():
        raise FileNotFoundError(f"Mapping file not found: {mapping_file}")

    file_config = json.loads(mapping_file.read_text())

    document_id = file_config.get("document_id")
    if not document_id:
        raise ValueError("document_id is required in the mapping file")
    mapping_ht = file_config.get("mapping")

    standardized = {}
    for target_field, source_field in mapping_ht.items():
        if source_field is None and target_field not in df.columns:
            standardized[target_field] = pd.Series([np.nan] * len(df))
            continue

        standardized[target_field] = df[source_field]

    treated_df = pd.DataFrame(standardized)
    treated_df["document_id"] = document_id
    treated_df["price"] = (
        treated_df["price"]
        .astype(str)
        .str.replace(" €", "")
        .str.replace(".", "")
        .str.replace(",", ".")
        .astype(float)
    )
    treated_df["item_code"] = treated_df["item_code"].astype(str)
    treated_df["invoice_number"] = treated_df["invoice_number"].astype(str)
    treated_df["customer_number"] = treated_df["customer_number"].astype(str)
    treated_df = add_missing_columns(treated_df)

    treated_df.dropna(subset=["item_description"], inplace=True)
    treated_df.drop_duplicates(inplace=True)
    return treated_df


def add_missing_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in required_columns:
        if col not in df.columns:
            df[col] = np.nan
    return df
