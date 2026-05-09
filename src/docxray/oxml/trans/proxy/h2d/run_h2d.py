from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_FORMAT
from docxray.oxml.trans.proxy.compute import on_off
from docxray.oxml.trans.proxy.document import Body
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import ParagraphStyle, TableStyle
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.styles import CT_TblStylePr

from .how_to_display import How2Display
from .run_rslv import RunResolver


class RunH2D(How2Display[RunResolver]):
    @cached_property
    def italic(self) -> bool:
        return self._display_toggled("i")

    @cached_property
    def bold(self) -> bool:
        return self._display_toggled("b")

    def _display_toggled(self, prop: str) -> bool:
        path = PropertyPath.base(prop, f"rPrDefault.{self._rslvr._path_base}")
        doc_val = self._rslvr._from_doc_dflts(path)
        if not isinstance(doc_val, NotFound):
            return on_off(doc_val)
        char_val: bool = getattr(self._rslvr, prop)
        prop_path = PropertyPath.base(
            "val", f"{self._rslvr._path_base}.{prop}"
        )
        para_val = False
        para_style = self._rslvr.para_style
        if para_style:
            para_val_got = self._value_from_para_style(
                para_style, prop_path, True
            )
            if not isinstance(para_val_got, NotFound):
                para_val = on_off(para_val_got)
        container = self._rslvr.paragraph.container
        if isinstance(container, Body):
            return para_val ^ char_val
        table_val = False
        table_val_got = self._value_from_tbl_style(container, prop_path, True)
        if not isinstance(table_val_got, NotFound):
            table_val = on_off(table_val_got)
        return table_val ^ para_val ^ char_val

    def _value_from_para_style(
        self,
        para_style: ParagraphStyle,
        prop_path: PropertyPath,
        prop_can_be_none: bool = False,
    ) -> NotFound | None:
        return self._rslvr._from_style_inheritance(
            para_style, prop_path, prop_can_be_none
        )

    # TODO: if needed - add fallback for base styles;
    # normally it's not a problem
    def _value_from_tbl_style(
        self,
        cell: Cell,
        prop_path: PropertyPath,
        prop_can_be_none: bool = False,
    ) -> NotFound | Any:
        tbl_style_props = cell.h2d._table_style_props
        tbl_style = cell.h2d._rslvr.table_style
        cnf = cell.h2d._cnf_gathered
        tbl_val = NotFound(cell, prop_path)
        while tbl_style_props and cnf:
            tbl_val = self._value_from_cnf(
                tbl_style_props, prop_path, prop_can_be_none
            )
            if tbl_val is None and prop_can_be_none:
                return tbl_val
            # Usually not called, but in very rare cases..
            tbl_style_props = self._tbl_style_props_from_base(tbl_style, cnf)
        if tbl_val is None and prop_can_be_none:
            return tbl_val
        if tbl_style is None:
            return tbl_val
        return self._rslvr._from_style_inheritance(
            tbl_style, prop_path, prop_can_be_none
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
        prop_can_be_none: bool = False,
    ) -> NotFound | Any:
        for tbl_style_prop in table_style_props:
            table_val = safe_get_prop(
                tbl_style_prop, prop_path, prop_can_be_none
            )
            if isinstance(table_val, NotFound):
                continue
            return table_val
        return NotFound(table_style_props, prop_path)
