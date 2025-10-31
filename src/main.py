import pandas as pd
from choose_files import select_extraction
from extract import (
    extract_specifications_for_constructions,
    extract_sample_invoice,
)
from transform.standardize_data import standardize_data
from load.load_documents import (
    load_documents,
)

file_name_to_function_ht = {
    "specifications_for_constructions": extract_specifications_for_constructions,
    "sample_invoice": extract_sample_invoice,
}


def main():
    file_paths = select_extraction()
    complete_standardized_df = pd.DataFrame()
    for file_path in file_paths:
        print(f"Extracting text from: {file_path.name}")
        print("-" * 50)
        extraction_function = file_name_to_function_ht.get(file_path.name)
        if not extraction_function:
            print(f"No extraction function defined for {file_path.name}")
            continue
        print("Extracting data...")
        extracted_df = extraction_function()
        print("Transforming data...")
        standardized_df = standardize_data(
            extracted_df, mapping_path=f"src/transform/configs/{file_path.name}.json"
        )
        complete_standardized_df = pd.concat(
            [complete_standardized_df, standardized_df], ignore_index=True
        )
    print("Loading data...")
    complete_standardized_df.to_csv("data/output/extracted_documents.csv", index=False)
    complete_standardized_df.to_parquet(
        "data/output/extracted_documents.parquet", index=False
    )
    load_documents(
        complete_standardized_df,
        table_name="extracted_documents",
        file_path="data/output/extracted_documents.sql",
    )


if __name__ == "__main__":
    main()
