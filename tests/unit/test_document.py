from pathlib import Path

from docxray import Document
from docxray.document import Document as D
from docxray.text.paragraph import Paragraph
from docxray.text.run import Run


class TestDocument:
    def test_open(self, test_file: Path) -> D:
        return Document(test_file)

    def test_iter_inner_content(self, test_file: Path) -> None:
        doc = self.test_open(test_file)
        for p_or_t in doc.iter_inner_content():
            if not isinstance(p_or_t, Paragraph):
                continue
            for r_or_h in p_or_t.iter_inner_content():
                if not isinstance(r_or_h, Run):
                    continue

                txt = r_or_h.raw_text
                elms = r_or_h.element.inner_content_items
