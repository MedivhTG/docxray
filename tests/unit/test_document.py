from pathlib import Path

from docxray import Document
from docxray.document import Document as D


class TestDocument:
    def test_open(self, test_file: Path) -> D:
        return Document(test_file)

    def test_iter_inner_content(self, test_file: Path) -> None:
        doc = self.test_open(test_file)
        for item in doc.iter_inner_content():
            pass
