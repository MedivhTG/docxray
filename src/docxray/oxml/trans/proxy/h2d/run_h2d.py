from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.compute import on_off
from docxray.oxml.trans.proxy.h2d.table_h2d import CellH2D
from docxray.oxml.trans.proxy.shared import NotFound
from docxray.oxml.trans.st.enums import (
    SE_OnOff1,
    SE_Underline,
    SE_VerticalAlignRun,
)

from .how_to_display import How2Display
from .run_rslv import RunResolver

type _OnOff = NotFound | bool | SE_OnOff1 | None


class RunH2D(How2Display[RunResolver]):
    @cached_property
    def cell_h2d(self) -> CellH2D | None:
        return self._rslvr.paragraph.h2d.cell_h2d

    @cached_property
    def italic(self) -> bool:
        return self._display_val_toggled("i")

    @cached_property
    def bold(self) -> bool:
        return self._display_val_toggled("b")

    @cached_property
    def all_uppercase(self) -> bool:
        return self._display_val_toggled("caps")

    @cached_property
    def all_downcase(self) -> bool:
        return self._display_val_toggled("smallCaps")

    @cached_property
    def single_strike_through(self) -> bool:
        return self._display_val_toggled("strike")

    # TODO: change after if needed
    @cached_property
    def underline(self) -> None | SE_Underline:
        line = self._display_val("u")
        if isinstance(line, NotFound) or line == SE_Underline.NONE:
            return None
        if line is None:
            return SE_Underline.SINGLE
        return line

    @cached_property
    def vertical_alignment(self) -> None | SE_VerticalAlignRun:
        align = self._display_val("vertAlign", False)
        if (
            isinstance(align, NotFound)
            or align == SE_VerticalAlignRun.BASELINE
        ):
            return None
        return align

    def _display_val(self, name: str, optional: bool = True) -> Any:
        char_val = self._rslvr.prop_val(name, optional, "both")
        if not isinstance(char_val, NotFound):
            return char_val
        para_val = self._rslvr.paragraph_resolver.prop_val_run(name, optional)
        if not isinstance(para_val, NotFound):
            return para_val
        char_path = self._rslvr.prop_path("val", f"rPr.{name}")
        c_h2d = self.cell_h2d
        if c_h2d:
            tbl_val, _ = self._rslvr.from_tbl_style_hierarchy(
                c_h2d._has_cnf,
                c_h2d._tbl_style_props_deep,
                char_path,
                optional,
            )
            return tbl_val
        doc_val_path = self._rslvr.prop_path(
            "val", f"rPrDefault.{self._rslvr._path_base}.{name}"
        )
        return self._rslvr.from_doc_dflts(doc_val_path, optional)

    def _display_val_toggled(self, name: str) -> bool:
        char_direct_val = self._rslvr.prop_val_toggled(name)
        if not isinstance(char_direct_val, NotFound):
            return on_off(char_direct_val)
        char_val = self._rslvr.prop_val_toggled(name, "style")
        para_val = self._rslvr.paragraph_resolver.prop_val_run_toggled(name)
        char_path = self._rslvr.prop_path("val", f"rPr.{name}")
        tbl_val = NotFound(self, char_path)
        c_h2d = self.cell_h2d
        if c_h2d:
            tbl_val, _ = self._rslvr.from_tbl_style_hierarchy(
                c_h2d._has_cnf,
                c_h2d._tbl_style_props_deep,
                char_path,
                True,
            )
        found_count = sum(
            1
            for i in [char_val, para_val, tbl_val]
            if not isinstance(i, NotFound)
        )
        if found_count > 1:
            return self._effective_toggled(name, char_val, para_val, tbl_val)
        if not isinstance(char_val, NotFound):
            return on_off(char_val)
        if not isinstance(para_val, NotFound):
            return on_off(para_val)
        if not isinstance(tbl_val, NotFound):
            return on_off(tbl_val)
        return False

    def _effective_toggled(
        self, name: str, char_val: _OnOff, para_val: _OnOff, tbl_val: _OnOff
    ) -> bool:
        doc_val_path = self._rslvr.prop_path(
            "val", f"rPrDefault.{self._rslvr._path_base}.{name}"
        )
        doc_val = on_off(self._rslvr.from_doc_dflts(doc_val_path, True))
        if doc_val is True:
            return doc_val
        return on_off(tbl_val) ^ on_off(para_val) ^ on_off(char_val)
