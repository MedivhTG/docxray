from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_TABLE_LOOK, CnfLookName
from docxray.oxml.trans.proxy.h2d.how2display import How2Display
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    TableStyle,
)
from docxray.oxml.trans.proxy.table import Row, Table
from docxray.oxml.trans.st.enums import SE_StyleType
from docxray.oxml.trans.table.row_props import CT_TblPrEx
from docxray.oxml.trans.table.table_props import CT_TblBorders


class RowH2D(How2Display[Row]):
    @cached_property
    def table(self) -> Table:
        return self._proxy.table

    @cached_property
    def first_row_show(self) -> bool:
        return self._format_from_cnf_look("firstRow")

    @cached_property
    def last_row_show(self) -> bool:
        return self._format_from_cnf_look("lastRow")

    @cached_property
    def first_col_show(self) -> bool:
        return self._format_from_cnf_look("firstColumn")

    @cached_property
    def last_col_show(self) -> bool:
        return self._format_from_cnf_look("lastColumn")

    @cached_property
    def no_horizontal_lines(self) -> bool:
        return self._format_from_cnf_look("noHBand")

    @cached_property
    def no_vertical_lines(self) -> bool:
        return self._format_from_cnf_look("noVBand")

    def _format_from_cnf_look(self, format_name: CnfLookName) -> bool:
        return self._cnf_look.has_format(format_name)

    @cached_property
    def _tblPrEx(self) -> CT_TblPrEx | None:
        tblPrEx_elm = self._prop("tblPrEx")
        if isinstance(tblPrEx_elm, NotFound):
            return None
        return tblPrEx_elm

    @cached_property
    def _table_style(self) -> TableStyle | None:
        if self._tblPrEx is None:
            return self.table.h2d._table_style
        style_id = safe_get_prop(
            self._tblPrEx, self._prop_path("val", "tblStyle"), False
        )
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.TABLE,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.TABLE],
        )

    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        if self._tblPrEx is None:
            return self.table.h2d._cnf_look
        mask: bytes | None = safe_get_prop(
            self._tblPrEx, self._prop_path("val", "tblLook")
        )
        if mask is None:
            return WD_CNF_TABLE_LOOK.from_bytes(b"")
        return WD_CNF_TABLE_LOOK.from_bytes(mask)

    @cached_property
    def _tblBorders(self) -> CT_TblBorders | None:
        if self._tblPrEx is not None:
            return self._tblPrEx.tblBorders
        return self.table.h2d._tblBorders

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self._table_style is None:
            return NotFound(self, path)
        return self._from_style_inheritance(self._table_style, path, optional)
