# backend/services/preprocessing.py

import re
from pathlib import Path

def clean_and_save_document(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Basic cleaning: remove extra whitespace, newlines, etc.
    cleaned = re.sub(r"\s+", " ", content).strip()

    cleaned_file = file_path.with_suffix(".cleaned.txt")
    with open(cleaned_file, "w", encoding="utf-8") as f:
        f.write(cleaned)

    return cleaned_file
