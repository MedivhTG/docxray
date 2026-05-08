from functools import cached_property

# docxray stuff
from docxray.oxml.trans.styles import CT_TblStylePr

from .how_to_display import How2Display
from .table_rslv import CellResolver, RowResolver, TableResolver


class TableH2D(How2Display[TableResolver]):
    pass


class RowH2D(How2Display[RowResolver]):
    pass


class CellH2D(How2Display[CellResolver]):
    @cached_property
    def _table_style_props(self) -> list[CT_TblStylePr]:
        tbl_style = self._rslvr.table_style
        if tbl_style is None:
            return []
        cnf = self._rslvr.cnf
        if cnf is None:
            return []
        return self._rslvr._table_style_props(tbl_style, cnf)
