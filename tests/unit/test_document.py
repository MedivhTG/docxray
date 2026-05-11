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
                part = p_or_t.part
                t_fmt = p_or_t.h2d
                for row in p_or_t.iter_rows():
                    part = row.part
                    for cell in row.iter_cells():
                        width = cell.width
                        is_last = cell.is_last
                        part = cell.part
                        cell_fmt = cell.h2d
                        cx = cell.grid_x
                        for p_or_t_inner in cell.iter_inner_content():
                            if isinstance(p_or_t_inner, Paragraph):
                                part = p_or_t_inner.part
                                p_fmt = p_or_t_inner.h2d
                                pPr = p_or_t_inner.element.pPr
                                if pPr is not None:
                                    spacing = pPr.spacing
                                for (
                                    r_or_h
                                ) in p_or_t_inner.iter_inner_content():
                                    if not isinstance(r_or_h, Run):
                                        continue
                                    part = r_or_h.part
                                    r_fmt = r_or_h.h2d
                                    italic = r_fmt.italic
                                    bold = r_fmt.bold
                                    caps = r_fmt.all_uppercase
                                    u = r_fmt.underline
                                    v_algn = r_fmt.vertical_alignment
                                    wait = 1
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
