from PyPDF2 import PdfReader

def parse_file(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()