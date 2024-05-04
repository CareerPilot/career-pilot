from pypdf import PdfReader
from docx import Document

def doc_to_text(doc_file_path):
    doc = Document(doc_file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])


def pdf_to_text(pdf_file_path: str) -> str:
    reader = PdfReader(pdf_file_path)
    text = '\n'.join(page.extract_text() for page in reader.pages)
    return text