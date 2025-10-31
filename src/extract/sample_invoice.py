import pdfplumber
import re
import pandas as pd


def extract_sample_invoice() -> pd.DataFrame:

    pdf_path = "data/input/sample_invoice.pdf"

    with pdfplumber.open(pdf_path) as pdf:
        main_page = pdf.pages[0]
        raw_page_tables = main_page.extract_tables()
        raw_text = main_page.extract_text()
        contract_infos = _get_infos_from_text(raw_text)

        general_informations_table = raw_page_tables[0]

        services_table = _extract_table_data(raw_page_tables[1])

        services_table.dropna(subset=["Service Description"], inplace=True)
        services_table["Invoice No"] = general_informations_table[1][0]
        services_table["Customer No"] = general_informations_table[1][1]
        services_table["Service Contractor"] = contract_infos["service_contractor_name"]
        services_table["Client Name"] = contract_infos["client_name"]
        services_table["VAT Percentage"] = contract_infos["vat_percentage"]
        services_table["Service Name"] = contract_infos["service_name"]

        services_table.to_parquet("data/sample_invoice_services.parquet", index=False)
        print(services_table.columns.tolist())
        return services_table


def _get_infos_from_text(text: str):

    service_name_match = re.search(r"invoice.+internet", text, flags=re.IGNORECASE)
    service_name = service_name_match.group(0) if service_name_match else "-"

    service_contractor_name_match = re.search(r"cpb.+gmbh", text, flags=re.IGNORECASE)
    service_contractor_name = (
        service_contractor_name_match.group(0) if service_contractor_name_match else "-"
    )

    client_name_match = re.search(r"Name: (.+)", text, flags=re.IGNORECASE)
    client_name = client_name_match.group(1) if client_name_match else "-"

    vat_percentage_match = re.search(r"VAT\s+(\d{1,2})\s*%", text, flags=re.IGNORECASE)
    vat_percentage = (
        int(vat_percentage_match.group(1)) if vat_percentage_match else None
    )

    return {
        "service_contractor_name": service_contractor_name,
        "client_name": client_name,
        "vat_percentage": vat_percentage * 0.01 if vat_percentage is not None else None,
        "service_name": service_name,
    }


def _extract_table_data(table: list[list[str]]) -> pd.DataFrame:
    df = pd.DataFrame(table[1:], columns=table[0])
    df = df.dropna(how="all")
    if df.empty:
        return pd.DataFrame()
    df = df.apply(lambda col: col.str.strip() if col.dtype == object else col)
    return df
