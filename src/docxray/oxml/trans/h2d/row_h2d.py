from functools import cached_property
from typing import Any, Literal

# docxray stuff
from docxray.oxml.trans.enums import (
    WD_CNF_FORMAT,
    WD_CNF_TABLE_LOOK,
    CnfLookName,
)
from docxray.oxml.trans.h2d.border import Border
from docxray.oxml.trans.h2d.how2display import How2Display
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import TableStyle
from docxray.oxml.trans.proxy.table import Row, Table
from docxray.oxml.trans.shared import CT_Shd, CT_TblWidth
from docxray.oxml.trans.st.enums import SE_TblStyleOverrideType
from docxray.oxml.trans.styles import CT_TblStylePr
from docxray.oxml.trans.table.table_props import (
    CT_JcTable,
    CT_TblBorders,
    CT_TblCellMar,
    CT_TblLayoutType,
)

type _TblBorder = Literal[
    "top", "bottom", "left", "right", "insideH", "insideV"
]


SHIFT_HORZ_BANDS = {
    SE_TblStyleOverrideType.HEADER_ROW,
    SE_TblStyleOverrideType.TOP_LEFT_CORNER_CELL,
    SE_TblStyleOverrideType.TOP_RIGHT_CORNER_CELL,
}
SHIFT_VERT_BANDS = {
    SE_TblStyleOverrideType.FIRST_COLUMN,
    SE_TblStyleOverrideType.TOP_LEFT_CORNER_CELL,
    SE_TblStyleOverrideType.BOTTOM_LEFT_CORNER_CELL,
}


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
    def _table_style(self) -> TableStyle | None:
        return self.table.h2d._table_style

    @cached_property
    def _latent_tbl_style_props(self) -> list[CT_TblStylePr]:
        if self._table_style is None:
            return []
        return self._table_style_props(self._table_style, WD_CNF_FORMAT(0xFFF))

    @cached_property
    def _shift_horz_bands(self) -> bool:
        for prop in self._latent_tbl_style_props:
            if prop.type in SHIFT_HORZ_BANDS:
                return True
        return False

    @cached_property
    def _shift_vert_bands(self) -> bool:
        for prop in self._latent_tbl_style_props:
            if prop.type in SHIFT_VERT_BANDS:
                return True
        return False

    @cached_property
    def _tblW(self) -> CT_TblWidth | None:
        return self._table_prop("tblW")

    @cached_property
    def _jc(self) -> CT_JcTable | None:
        return self._table_prop("jc")

    @cached_property
    def _tblCellSpacing(self) -> CT_TblWidth | None:
        return self._table_prop("tblCellSpacing")

    @cached_property
    def _tblInd(self) -> CT_TblWidth | None:
        return self._table_prop("tblInd")

    @cached_property
    def _tblBorders(self) -> CT_TblBorders | None:
        return self._table_prop("tblBorders")

    @cached_property
    def _table_top(self) -> Border | None:
        return self._table_border("top")

    @cached_property
    def _table_bottom(self) -> Border | None:
        return self._table_border("bottom")

    @cached_property
    def _table_left(self) -> Border | None:
        return self._table_border("left")

    @cached_property
    def _table_right(self) -> Border | None:
        return self._table_border("right")

    @cached_property
    def _table_insideH(self) -> Border | None:
        return self._table_border("insideH")

    @cached_property
    def _table_insideV(self) -> Border | None:
        return self._table_border("insideV")

    @cached_property
    def _shd(self) -> CT_Shd | None:
        return self._table_prop("shd")

    @cached_property
    def _tblLayout(self) -> CT_TblLayoutType | None:
        return self._table_prop("tblLayout")

    @cached_property
    def _tblCellMar(self) -> CT_TblCellMar | None:
        return self._table_prop("tblCellMar")

    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        mask = self._prop_val(self._prop_path("val", "tblPrEx.tblLook"))
        if not isinstance(mask, NotFound):
            WD_CNF_TABLE_LOOK.from_bytes(mask)
        return self.table.h2d._cnf_look

    def _table_prop(self, name: str) -> Any:
        path = self._prop_path(name, "tblPrEx")
        prop = safe_get_prop(self._proxy.element, path, False)
        if isinstance(prop, NotFound):
            return self.table.h2d._table_prop(name)
        return prop

    def _table_border(self, side: _TblBorder) -> Border | None:
        side_elm = safe_get_prop(
            self._tblBorders, PropertyPath.base(side), False
        )
        if not isinstance(side_elm, NotFound):
            return Border(side_elm, self._proxy)
        return None

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self._table_style is None:
            return NotFound(self, path)
        return self._from_style_inheritance(self._table_style, path, optional)
