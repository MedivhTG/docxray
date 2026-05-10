from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_FORMAT
from docxray.oxml.trans.proxy.compute import on_off
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
    pass


class RowH2D(How2Display[RowResolver]):
    pass


class CellH2D(How2Display[CellResolver]):
    @cached_property
    def _table_style_props(self) -> list[CT_TblStylePr]:
        tbl_style = self._rslvr.table_style
        if tbl_style is None:
            return []
        cnf_gathered = self._cnf_gathered
        if cnf_gathered is None:
            return []
        return self._rslvr._table_style_props(tbl_style, cnf_gathered)

    @cached_property
    def _cnf_gathered(self) -> WD_CNF_FORMAT | None:
        cnf_cell = self._rslvr._cnf
        cnf_row = self._rslvr._cnf_row
        cnf = cnf_cell
        if cnf_row is not None:
            if cnf is None:
                cnf = cnf_row
            else:
                cnf |= cnf_row
        if cnf is None:
            return None
        return self._cnf_from_tbl_look(cnf)

    # --- Properties for Run
    def _prop_val_for_rpr(self, name: str, toggled: bool) -> NotFound | Any:
        path = self._rslvr._prop_path("val", f"rPr.{name}")
        val = self._value_from_tbl_style(path, toggled)
        if toggled:
            if isinstance(val, NotFound):
                return val
            return on_off(val)
        return val

    @cached_property
    def _i(self) -> bool | NotFound:
        return self._prop_val_for_rpr("i", True)

    @cached_property
    def _b(self) -> bool | NotFound:
        return self._prop_val_for_rpr("b", True)

    @cached_property
    def _caps(self) -> bool | NotFound:
        return self._prop_val_for_rpr("caps", True)

    # ---

    def _value_from_tbl_style(
        self,
        prop_path: PropertyPath,
        prop_optional: bool = False,
    ) -> Any:
        tbl_style_props = self._table_style_props
        tbl_style = self._rslvr.table_style
        cnf = self._cnf_gathered
        tbl_val = NotFound(self, prop_path)
        while tbl_style_props and cnf:
            tbl_val = self._value_from_cnf(
                tbl_style_props, prop_path, prop_optional
            )
            if tbl_val is None and prop_optional:
                return tbl_val
            # Usually not called, but in very rare cases..
            tbl_style_props = self._tbl_style_props_from_base(tbl_style, cnf)
        if tbl_val is None and prop_optional:
            return tbl_val
        if tbl_style is None:
            return tbl_val
        return self._rslvr._from_style_inheritance(
            tbl_style, prop_path, prop_optional
        )

    def _tbl_style_props_from_base(
        self, tbl_style: TableStyle | None, cnf: WD_CNF_FORMAT
    ) -> list[CT_TblStylePr]:
        if tbl_style is None:
            return []
        base_style = self._rslvr._styles.base_style(tbl_style)
        if not isinstance(base_style, TableStyle):
            return []
        return self._rslvr._table_style_props(base_style, cnf)

    def _value_from_cnf(
        self,
        table_style_props: list[CT_TblStylePr],
        prop_path: PropertyPath,
        prop_optional: bool = False,
    ) -> Any:
        for tbl_style_prop in table_style_props:
            table_val = safe_get_prop(tbl_style_prop, prop_path, prop_optional)
            if isinstance(table_val, NotFound):
                continue
            return table_val
        return NotFound(table_style_props, prop_path)

    def _cnf_from_tbl_look(self, cnf: WD_CNF_FORMAT) -> WD_CNF_FORMAT:
        row_rslvr = self._rslvr.row_resolver
        if not row_rslvr.first_row_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
        if not row_rslvr.last_row_show:
            cnf &= ~WD_CNF_FORMAT.LAST_ROW
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if not row_rslvr.first_col_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
        if not row_rslvr.last_col_show:
            cnf &= ~WD_CNF_FORMAT.LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if row_rslvr.no_horizontal_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_HORIZONTAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND
        if row_rslvr.no_vertical_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_VERTICAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_VERTICAL_BAND
        return cnf
