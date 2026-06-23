from pypdf import PdfReader

def extract_text(path: str):
    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text