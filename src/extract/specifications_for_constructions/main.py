import pdfplumber
import re
import pandas as pd


def extract_text_from_pdf(pdf_path: str) -> pd.DataFrame:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    parsed_data = _get_construction_sections(text)
    parsed_data["description"] = parsed_data.apply(
        lambda row: _get_description_by_section(
            row["section_name"], row["section_code"], text
        ),
        axis=1,
    )
    return parsed_data


def _get_construction_sections(text: str) -> pd.DataFrame:

    title_match = re.search(r".*Specifications for Construction.*", text)
    title = title_match.group(0).strip() if title_match else "-"

    city_match = re.search(r"city of\s+([A-Za-z\s,]+)", text)
    city = city_match.group(1).strip() if city_match else "-"

    year_match = re.search(r"[21][90]\d{2}", text)
    year = int(year_match.group(0)) if year_match else None

    author_match = re.search(r"[A-Za-z\s,]*Inc\.", text)
    author = author_match.group(0).strip() if author_match else "-"

    sections = re.findall(r"(\d{5,6})\s*-\s*([A-Za-z].+)", text)
    sections = [
        {
            "section_code": code,
            "section_name": name.strip(),
            "title": title.strip(),
            "city": city,
            "year": year,
            "author": author,
        }
        for code, name in sections
    ]

    sections_df = pd.DataFrame(sections)

    return sections_df


def _get_description_by_section(section_name: str, section_code: str, text: str) -> str:
    if section_code in ["00005", "00010", "00700"]:
        return ""
    pattern = (
        rf"section\s+{section_code}.+{re.escape(section_name)}(.*)"
        r"\*\*\*\*END OF SECTION\*\*\*\*"
    )
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return ""
    description = match.group(1).strip()
    return description
