from pathlib import Path


UPLOAD_FOLDER = Path(__file__).resolve().parents[2] / "storage" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file_name: str, file_bytes: bytes) -> Path:
    safe_name = file_name.replace("/", "_").replace("\\", "_")
    output_path = UPLOAD_FOLDER / safe_name
    output_path.write_bytes(file_bytes)
    return output_path


def extract_text_from_pdf_placeholder(file_path: Path) -> str:
    return f"PDF extraction not connected yet for {file_path.name}. Add pypdf here."


def extract_text_from_image_placeholder(file_path: Path) -> str:
    return f"OCR is not connected yet for {file_path.name}. Add pytesseract here."
