from pathlib import Path

from docxray import Document
from docxray.oxml.trans.proxy.shared import Length
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
                        # _f = cell.cell_below.cell_next
                        # _f_1 = _f.grid_x
                        # _f_2 = _f.grid_y
                        # _f_3 = _f.cell_above
                        # _f_4 = _f.cell_below
                        # _f_5 = _f.cell_next
                        # _f_6 = _f.cell_prev
                        # _f_7 = _f.idx
                        # _f_8 = _f.is_first
                        # _f_9 = _f.is_last
                        # _f_10 = _f.vert_span
                        # _f_11 = _f.horz_span
                        cell_fmt = cell.h2d
                        cx = cell.grid_x
                        cy = cell.grid_y
                        borders_inf = cell_fmt.borders_info
                        wait = 1
                        for p_or_t_inner in cell.iter_inner_content():
                            if isinstance(p_or_t_inner, Paragraph):
                                part = p_or_t_inner.part
                                p_fmt = p_or_t_inner.h2d
                                pPr = p_or_t_inner.element.pPr
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
                align = p_fmt.alignment
                no_hanging = p_fmt.no_hanging
                left = (
                    p_fmt.margin_line_start.cm
                    if isinstance(p_fmt.margin_line_start, Length)
                    else p_fmt.margin_line_start
                )
                lvl = p_fmt.header_level
                para_Style_num = p_fmt._para_style_numbering
                pPr = p_or_t.element.pPr
                if pPr is not None:
                    w = 1
                for r_or_h in p_or_t.iter_inner_content():
                    if not isinstance(r_or_h, Run):
                        continue
                    part = r_or_h.part
                    r_fmt = r_or_h.h2d
                    italic = r_fmt.italic
                    bold = r_fmt.bold
                    wait = 1
