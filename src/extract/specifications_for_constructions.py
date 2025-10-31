import pdfplumber
import re
import pandas as pd


def extract_specifications_for_constructions() -> pd.DataFrame:
    pdf_path = "data/input/specifications_for_constructions.pdf"
    text, text_by_page = _get_page_text(pdf_path)
    parsed_data = _get_construction_sections(text)
    parsed_data.dropna(subset=["section_code", "section_name"], inplace=True)
    parsed_data[["details", "page_codes"]] = parsed_data.apply(
        lambda row: _get_description_by_section(row["section_code"], text_by_page),
        axis=1,
    )
    return parsed_data


def _get_page_text(pdf_path: str) -> list[tuple[str, str]]:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        text_by_page = []
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text
            page_id_match = re.search(
                r"PAGE\W*([0-9]{1,6}\s?-\s?[0-9]{1,4})", page_text, flags=re.IGNORECASE
            )
            if page_id_match:
                page_id = page_id_match.group(1)
                text_by_page.append((page_id, page_text))
    return (text, text_by_page)


def _get_construction_sections(text: str) -> pd.DataFrame:

    title_match = re.search(
        r".*Specifications for Construction.*", text, flags=re.IGNORECASE
    )
    title = title_match.group(0).strip() if title_match else "-"

    city_match = re.search(r"city of\s+([A-Za-z\s,]+)", text, flags=re.IGNORECASE)
    city = city_match.group(1).strip() if city_match else "-"

    author_match = re.search(r".+Inc\.", text)
    author = author_match.group(0).strip() if author_match else "-"

    sections = re.findall(r"(\d{5,6})\s*-\s*([A-Za-z].+)", text)
    sections = [
        {
            "section_code": code,
            "section_name": name.strip(),
            "title": title.strip(),
            "city": city,
            "author": author,
        }
        for code, name in sections
    ]

    sections_df = pd.DataFrame(sections)

    sections_df.drop_duplicates(subset=["section_code", "section_name"], inplace=True)

    return sections_df


def _get_description_by_section(
    section_code: str, text_page: list[tuple[str, str]]
) -> str:
    page_text = ""
    page_codes = []
    for page_id, page_content in text_page:
        if page_id.startswith(section_code):
            page_text += page_content
            page_codes.append(page_id)

    return pd.Series({"details": page_text, "page_codes": page_codes})
