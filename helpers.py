import itertools as it

import docx
from pypdf import PdfReader


def doc_to_text(doc_file_path: str) -> str:
    def item_to_text(tp) -> str:
        if type(tp) == docx.text.paragraph.Paragraph:
            text = tp.text
        elif type(tp) == docx.table.Table:
            g = (s for s, _ in it.groupby(c.text for r in tp.rows for c in r.cells))
            text = "\n".join(filter(None, g))
        else:
            raise ValueError(f"unexpected {type(tp)} object in document")
        return text

    doc = docx.Document(doc_file_path)
    g = (tp for s in doc.sections for tp in s.iter_inner_content())
    text = "\n".join(item_to_text(tp) for tp in g)
    return text


def pdf_to_text(pdf_file_path: str) -> str:
    reader = PdfReader(pdf_file_path)
    text = "\n".join(page.extract_text() for page in reader.pages)
    return text
