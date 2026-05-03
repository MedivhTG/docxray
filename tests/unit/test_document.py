from pathlib import Path

from docxray import Document
from docxray.document import Document as D
from docxray.table import Table
from docxray.text.paragraph import Paragraph
from docxray.text.run import Run


class TestDocument:
    def test_open(self, test_file: Path) -> D:
        return Document(test_file)

    def test_iter_inner_content(self, test_file: Path) -> None:
        doc = self.test_open(test_file)
        part = doc.part
        for p_or_t in doc.iter_inner_content():
            if isinstance(p_or_t, Table):
                part = p_or_t.part
                t_fmt = p_or_t.resolver
                for row in p_or_t.iter_rows():
                    for cell in row.iter_cells():
                        for p_or_t in cell.iter_inner_content():
                            if isinstance(p_or_t, Paragraph):
                                part = p_or_t.part
                                p_fmt = p_or_t.resolver
                                for r_or_h in p_or_t.iter_inner_content():
                                    if not isinstance(r_or_h, Run):
                                        continue
                                    part = r_or_h.part
                                    r_fmt = r_or_h.resolver
                                    italic = r_fmt.italic
                                    italic2 = r_fmt.italic
                                    wait = 1
            elif isinstance(p_or_t, Paragraph):
                part = p_or_t.part
                p_fmt = p_or_t.resolver
                for r_or_h in p_or_t.iter_inner_content():
                    if not isinstance(r_or_h, Run):
                        continue
                    part = r_or_h.part
                    r_fmt = r_or_h.resolver
                    italic = r_fmt.italic
                    italic2 = r_fmt.italic
                    wait = 1
