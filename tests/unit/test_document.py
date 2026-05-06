from pathlib import Path

from docxray import Document
from docxray.document import Document as D
from docxray.table import Table
from docxray.text.paragraph import Paragraph
from docxray.text.run import Run


class TestDocument:
    def test_open(self, test_file: Path) -> None:
        doc = Document(test_file)
        assert doc is not None

    def test_iter_inner_content(self, test_file: Path) -> None:
        doc = Document(test_file)
        part = doc.part
        for p_or_t in doc.iter_inner_content():
            if isinstance(p_or_t, Table):
                part = p_or_t.part
                t_fmt = p_or_t.resolver
                for row in p_or_t.iter_rows():
                    part = row.part
                    for cell in row.iter_cells():
                        is_last = cell.element.is_last
                        part = cell.part
                        cell_fmt = cell.resolver
                        cx = cell.grid_x
                        for p_or_t in cell.iter_inner_content():
                            if isinstance(p_or_t, Paragraph):
                                part = p_or_t.part
                                p_fmt = p_or_t.resolver
                                pPr = p_or_t.element.pPr
                                if pPr is not None:
                                    spacing = pPr.spacing
                                for r_or_h in p_or_t.iter_inner_content():
                                    if not isinstance(r_or_h, Run):
                                        continue
                                    part = r_or_h.part
                                    r_fmt = r_or_h.resolver
                                    italic = r_fmt.italic
                                    italic2 = r_fmt.italic
                                    bold = r_fmt.bold
                                    wait = 1
            elif isinstance(p_or_t, Paragraph):
                f = p_or_t.element.is_first
                part = p_or_t.part
                p_fmt = p_or_t.resolver
                in_list = p_fmt.in_list
                outl = p_fmt.outline_lvl
                pPr = p_or_t.element.pPr
                if pPr is not None:
                    spacing = pPr.spacing
                    w = 1
                for r_or_h in p_or_t.iter_inner_content():
                    if not isinstance(r_or_h, Run):
                        continue
                    part = r_or_h.part
                    r_fmt = r_or_h.resolver
                    italic = r_fmt.italic
                    italic2 = r_fmt.italic
                    bold = r_fmt.bold
                    v_align = r_fmt.vertical_align
                    u = r_fmt.underline
                    wait = 1
