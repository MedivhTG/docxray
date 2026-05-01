from pathlib import Path

from docxray import Document

path = Path(__file__).parent / "examples" / "abc.docx"

doc = Document(path)
blob = doc.element
wait = 1
