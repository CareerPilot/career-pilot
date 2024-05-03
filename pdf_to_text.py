from pypdf import PdfReader

def pdf_to_text(pdf_file_path: str) -> str:
    reader = PdfReader(pdf_file_path)
    text = '\n'.join(page.extract_text() for page in reader.pages)
    return text
