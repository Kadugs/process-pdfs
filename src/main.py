from extract.specifications_for_constructions.main import extract_text_from_pdf


def main():
    pdf_path = "data/input/specifications-for-constructions.pdf"
    df = extract_text_from_pdf(pdf_path)
    df.to_parquet("data/output.parquet", index=False)
    print("Extracted data saved to data/output.parquet")


if __name__ == "__main__":
    main()
