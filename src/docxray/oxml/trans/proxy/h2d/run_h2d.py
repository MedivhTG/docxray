from functools import cached_property
from typing import Any, cast

# docxray stuff
from docxray.oxml.trans.proxy.document import Body
from docxray.oxml.trans.proxy.shared import PropertyPath, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import ParagraphStyle, TableStyle
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.styles import CT_TblStylePr

from .how_to_display import How2Display
from .run_rslv import RunResolver


class RunH2D(How2Display[RunResolver]):
    @cached_property
    def italic(self) -> bool:
        return self._display_toggled("i")

    def _display_toggled(self, prop: str) -> bool:
        path = PropertyPath.base(prop, f"rPrDefault.{self._rslvr._path_base}")
        doc_val = self._rslvr._from_doc_dflts(path)
        if doc_val is not None:
            return bool(doc_val)
        char_val = bool(getattr(self._rslvr, prop))
        prop_path = PropertyPath.base(
            "val", f"{self._rslvr._path_base}.{prop}"
        )
        para_val = False
        para_style = self._rslvr.para_style
        if para_style:
            para_val = bool(self._value_from_para_style(para_style, prop_path))
        container = self._rslvr.paragraph.container
        if isinstance(container, Body):
            return para_val ^ char_val
        table_val = bool(self._value_from_table_style(container, prop_path))
        return table_val ^ para_val ^ char_val

    def _value_from_para_style(
        self, para_style: ParagraphStyle, prop_path: PropertyPath
    ) -> Any | None:
        return self._rslvr._from_style_inheritance(para_style, prop_path)

    def _value_from_table_style(
        self, cell: Cell, property_path: PropertyPath
    ) -> Any | None:
        tbl_style_props = cell.h2d._table_style_props
        if tbl_style_props:
            return self._value_from_cnf(cell, property_path)
        tbl_style = cell.h2d._rslvr.table_style
        if tbl_style is None:
            return None
        return self._rslvr._from_style_inheritance(tbl_style, property_path)

    def _value_from_cnf(
        self, cell: Cell, prop_path: PropertyPath
    ) -> Any | None:
        tbl_style_props = cell.h2d._table_style_props
        table_val = self._value_from_cnf_pattern(tbl_style_props, prop_path)
        if table_val is not None:
            return table_val
        # Fallback for edge cases:
        # in common Word will not produce inherited table styles without
        # cnf from basedOn style (always copy and override)
        tbl_style = cell.h2d._rslvr.table_style
        if tbl_style is None:
            return table_val
        tbl_style = cast(
            "TableStyle | None", self._rslvr._styles.base_style(tbl_style)
        )
        if tbl_style is None:
            return table_val
        cnf = cell.h2d._rslvr.cnf
        if cnf is None:
            return table_val
        while table_val is None:
            tbl_style_props = self._rslvr._table_style_props(tbl_style, cnf)
            table_val = self._value_from_cnf_pattern(
                tbl_style_props, prop_path
            )
            base_style = self._rslvr._styles.base_style(tbl_style)
            if not isinstance(base_style, tbl_style.__class__):
                return table_val
            tbl_style = base_style
        return table_val

    def _value_from_cnf_pattern(
        self, tbl_style_props: list[CT_TblStylePr], prop_path: PropertyPath
    ) -> Any | None:
        for tbl_style_prop in tbl_style_props:
            table_val = safe_get_prop(tbl_style_prop, prop_path)
            if table_val is not None:
                return table_val
        return None
