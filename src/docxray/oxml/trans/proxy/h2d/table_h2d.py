from functools import cached_property

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_FORMAT
from docxray.oxml.trans.styles import CT_TblStylePr

from .how_to_display import How2Display
from .table_rslv import CellResolver, RowResolver, TableResolver


class TableH2D(How2Display[TableResolver]):
    pass


# TODO: Some props can be overriden by tblPrEx in row,
# look for adding this elm it in ECMA-376 documents (do after)
class RowH2D(How2Display[RowResolver]):
    pass


class CellH2D(How2Display[CellResolver]):
    @cached_property
    def _table_style_props(self) -> list[CT_TblStylePr]:
        tbl_style = self._rslvr.table_style
        if tbl_style is None:
            return []
        cell_cnf = self._rslvr.cnf
        row_cnf = self._rslvr.row_cnf
        cnf = cell_cnf
        if row_cnf is not None and cnf is not None:
            cnf |= row_cnf
        else:
            cnf = row_cnf
        if cnf is None:
            return []
        cnf_looked = self._cnf_from_tbl_look(cnf)
        return self._rslvr._table_style_props(tbl_style, cnf_looked)

    def _cnf_from_tbl_look(self, cnf: WD_CNF_FORMAT) -> WD_CNF_FORMAT:
        tbl_rslvr = self._rslvr.table_resolver
        if not tbl_rslvr.first_row_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
        if not tbl_rslvr.last_row_show:
            cnf &= ~WD_CNF_FORMAT.LAST_ROW
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if not tbl_rslvr.first_col_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
        if not tbl_rslvr.last_col_show:
            cnf &= ~WD_CNF_FORMAT.LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if tbl_rslvr.no_horizontal_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_HORIZONTAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND
        if tbl_rslvr.no_vertical_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_VERTICAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_VERTICAL_BAND
        return cnf
