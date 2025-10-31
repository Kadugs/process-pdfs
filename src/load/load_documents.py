from typing import List

import pandas as pd


def load_documents(df: pd.DataFrame, table_name: str, file_path: str) -> None:
    export_dataframe_to_sql_dump(df, table_name, file_path)
    print(f"SQL dump written to {file_path}")


def export_dataframe_to_sql_dump(
    df: pd.DataFrame,
    table_name: str,
    file_path: str,
    include_create: bool = True,
    if_exists: str = "replace",
    batch_size: int = 500,
) -> None:
    df = df.copy()
    df.columns = [str(c) for c in df.columns]

    with open(file_path, "w", encoding="utf-8") as f:
        if include_create:
            if if_exists == "replace":
                f.write(f'DROP TABLE IF EXISTS "{table_name}";\n')
            cols = []
            for col in df.columns:
                col_type = _sql_type_for_series(df[col])
                cols.append(f'  "{col}" {col_type}')
            cols_sql = ",\n".join(cols)
            f.write(f'CREATE TABLE "{table_name}" (\n{cols_sql}\n);\n\n')

        if df.empty:
            return

        cols_quoted = ", ".join([f'"{c}"' for c in df.columns])
        for start in range(0, len(df), batch_size):
            chunk = df.iloc[start : start + batch_size]
            values_lines = []
            for _, row in chunk.iterrows():
                vals = [_format_value(x) for x in row.tolist()]
                values_lines.append(f"({', '.join(vals)})")
            values_sql = ",\n".join(values_lines)
            insert_sql = (
                f'INSERT INTO "{table_name}" ({cols_quoted}) VALUES\n'
                f"{values_sql};\n\n"
            )
            f.write(insert_sql)


def _format_value(value) -> str:
    if value is None:
        return "NULL"
    if pd.isna(value):
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int,)) and not isinstance(value, bool):
        return str(int(value))
    if isinstance(value, float):
        return repr(float(value))
    s = str(value)
    s = s.replace("'", "''")
    return f"'{s}'"


def _sql_type_for_series(series: pd.Series) -> str:
    types = pd.api.types
    if types.is_string_dtype(series.dtype):
        return "TEXT"
    if types.is_integer_dtype(series.dtype):
        return "BIGINT"
    if types.is_float_dtype(series.dtype):
        return "DOUBLE PRECISION"
    if types.is_bool_dtype(series.dtype):
        return "BOOLEAN"
    if types.is_datetime64_any_dtype(series.dtype):
        return "TIMESTAMP"
    return "TEXT"
