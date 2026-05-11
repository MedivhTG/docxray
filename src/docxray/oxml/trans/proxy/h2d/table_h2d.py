from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.enums import (
    WD_CNF_FORMAT,
    WD_CNF_TABLE_LOOK,
    CnfLookName,
)
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import TableStyle
from docxray.oxml.trans.styles import CT_TblStylePr

from .how_to_display import How2Display
from .table_rslv import CellResolver, RowResolver, TableResolver


class TableH2D(How2Display[TableResolver]):
    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        mask: bytes | None = self._rslvr.prop_val("tblLook", optional=True)
        if mask is None:
            return WD_CNF_TABLE_LOOK.from_bytes(b"")
        return WD_CNF_TABLE_LOOK.from_bytes(mask)


class RowH2D(How2Display[RowResolver]):
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
    def _cnf(self) -> WD_CNF_FORMAT | None:
        cnf = self._rslvr.prop_val("cnfStyle")
        if isinstance(cnf, NotFound):
            return None
        return WD_CNF_FORMAT.from_string(cnf)

    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        if self._rslvr.tblPrEx is None:
            return self._rslvr.table.h2d._cnf_look
        mask: bytes | None = safe_get_prop(
            self._rslvr.tblPrEx, self._rslvr.prop_path("val", "tblLook")
        )
        if mask is None:
            return WD_CNF_TABLE_LOOK.from_bytes(b"")
        return WD_CNF_TABLE_LOOK.from_bytes(mask)


class CellH2D(How2Display[CellResolver]):
    @cached_property
    def _cnf(self) -> WD_CNF_FORMAT | None:
        cnf = self._rslvr.prop_val("cnfStyle")
        if isinstance(cnf, NotFound):
            return None
        return WD_CNF_FORMAT.from_string(cnf)

    @cached_property
    def _cnf_row(self) -> WD_CNF_FORMAT | None:
        return self._rslvr.row.h2d._cnf

    @cached_property
    def _cnf_gathered(self) -> WD_CNF_FORMAT | None:
        cnf_cell = self._cnf
        cnf_row = self._cnf_row
        cnf = cnf_cell
        if cnf_row is not None:
            if cnf is None:
                cnf = cnf_row
            else:
                cnf |= cnf_row
        if cnf is None:
            return None
        return self._cnf_looked(cnf)

    @cached_property
    def _has_cond_format(self) -> bool:
        return False if self._cnf_gathered is None else True

    @cached_property
    def _tbl_style_props_deep(
        self,
    ) -> list[tuple[TableStyle, list[CT_TblStylePr]]]:
        tbl_style = self._rslvr.table_style
        props_leveled = []
        cnf = self._cnf_gathered
        while isinstance(tbl_style, TableStyle):
            if cnf is not None:
                tbl_style_props = self._rslvr.table_style_props(tbl_style, cnf)
            else:
                tbl_style_props = []
            props_leveled.append((tbl_style, tbl_style_props))
            tbl_style = self._rslvr._styles.base_style(tbl_style)  # type: ignore[assignment]
        return props_leveled

    def _from_tbl_style_hierarchy(
        self, path: PropertyPath, optional: bool = False
    ) -> Any:
        style_direct_val = NotFound(self, path)
        for tbl_style, tbl_style_props in self._tbl_style_props_deep:
            if self._has_cond_format:
                if isinstance(style_direct_val, NotFound):
                    style_direct_val = safe_get_prop(
                        tbl_style.element, path, optional
                    )
                tbl_val = self._from_tbl_style_props(
                    tbl_style_props, path, optional
                )
                if not isinstance(tbl_val, NotFound):
                    return tbl_val
            else:
                tbl_val = safe_get_prop(tbl_style.element, path, optional)
                if not isinstance(tbl_val, NotFound):
                    return tbl_val
        return style_direct_val

    def _from_tbl_style_props(
        self,
        table_style_props: list[CT_TblStylePr],
        path: PropertyPath,
        optional: bool = False,
    ) -> Any:
        for tbl_style_prop in table_style_props:
            table_val = safe_get_prop(tbl_style_prop, path, optional)
            if isinstance(table_val, NotFound):
                continue
            return table_val
        return NotFound(table_style_props, path)

    def _cnf_looked(self, cnf: WD_CNF_FORMAT) -> WD_CNF_FORMAT:
        row_h2d = self._rslvr.row.h2d
        if not row_h2d.first_row_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
        if not row_h2d.last_row_show:
            cnf &= ~WD_CNF_FORMAT.LAST_ROW
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if not row_h2d.first_col_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
        if not row_h2d.last_col_show:
            cnf &= ~WD_CNF_FORMAT.LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if row_h2d.no_horizontal_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_HORIZONTAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND
        if row_h2d.no_vertical_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_VERTICAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_VERTICAL_BAND
        return cnf
