from docx_parser import DocumentParser
from pypdf import PdfReader

def doc_to_text(doc_file_path: str) -> str:
    def item_to_text(itemType, item) -> str:
        if itemType == 'multipart':
            text = '\n'.join(s for s in item if type(s) == str)
        elif itemType == 'paragraph':
            text = item['text']
        elif itemType == 'table':
            g = (s for s, _ in it.groupby(it.chain.from_iterable(item['data'])))
            text = '\n'.join(filter(None, g))
        return text
    doc = DocumentParser(doc_file_path)
    text = '\n'.join(item_to_text(*t) for t in doc.parse())
    return text

def pdf_to_text(pdf_file_path: str) -> str:
    reader = PdfReader(pdf_file_path)
    text = '\n'.join(page.extract_text() for page in reader.pages)
    return text
