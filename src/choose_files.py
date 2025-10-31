from pathlib import Path
import inquirer
import re


def select_extraction() -> Path:
    input_dir = Path("src/extract")
    possibilities = input_dir.glob("*.py")

    options = [
        re.sub(r"\.py$", "", p.name) for p in possibilities if p.name != "__init__.py"
    ]

    all_options = options + ["All Files", "Cancel"]
    question = [
        inquirer.List("file", message="Select PDF to process", choices=all_options)
    ]
    answer = inquirer.prompt(question)
    if answer["file"] == "Cancel":
        print("operation cancelled")
        exit(0)
    if answer["file"] == "All Files":
        print("all files selected")
        return [input_dir / option for option in options]
    return [input_dir / answer["file"]]
