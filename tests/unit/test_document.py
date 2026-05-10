from pathlib import Path

from docxray import Document
from docxray.oxml.trans.proxy.table import Table
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.proxy.text.run import Run


class TestDocument:
    def test_open(self, test_file: Path) -> None:
        doc = Document(test_file)
        assert doc is not None

    def test_iter_inner_content(self, test_file: Path) -> None:
        doc = Document(test_file)
        part = doc.part
        for p_or_t in doc.iter_inner_content():
            if isinstance(p_or_t, Table):
                pass
            elif isinstance(p_or_t, Paragraph):
                f = p_or_t.element.is_first
                part = p_or_t.part
                p_fmt = p_or_t.h2d
                pPr = p_or_t.element.pPr
                if pPr is not None:
                    spacing = pPr.spacing
                    w = 1
                for r_or_h in p_or_t.iter_inner_content():
                    if not isinstance(r_or_h, Run):
                        continue
                    part = r_or_h.part
                    r_fmt = r_or_h.h2d
                    italic = r_fmt.italic
                    wait = 1
