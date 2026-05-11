from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.compute import on_off
from docxray.oxml.trans.proxy.h2d.table_h2d import CellH2D
from docxray.oxml.trans.proxy.shared import NotFound
from docxray.oxml.trans.st.enums import SE_OnOff1

from .how_to_display import How2Display
from .run_rslv import RunResolver

type _OnOff = NotFound | bool | SE_OnOff1 | None


class RunH2D(How2Display[RunResolver]):
    @cached_property
    def cell_h2d(self) -> CellH2D | None:
        return self._rslvr.paragraph.h2d.cell_h2d

    @cached_property
    def italic(self) -> bool:
        return self._display_toggled("i")

    @cached_property
    def bold(self) -> bool:
        return self._display_toggled("b")

    @cached_property
    def all_uppercase(self) -> bool:
        return self._display_toggled("caps")

    @cached_property
    def all_downcase(self) -> bool:
        return self._display_toggled("smallCaps")

    @cached_property
    def single_strike_through(self) -> bool:
        return self._display_toggled("strike")

    def _display_toggled(self, name: str) -> bool:
        char_direct_val = self._rslvr.prop_val_toggled(name)
        if not isinstance(char_direct_val, NotFound):
            return on_off(char_direct_val)
        char_val = self._rslvr.prop_val_toggled(name, "style")
        para_val = self._rslvr.paragraph_resolver.prop_val_run_toggled(name)
        char_path = self._rslvr.prop_path("val", f"rPr.{name}")
        tbl_val = NotFound(self, char_path)
        if self.cell_h2d:
            tbl_val = self.cell_h2d._from_tbl_style_hierarchy(char_path, True)
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
        doc_path = self._rslvr.prop_path(
            "val", f"rPrDefault.{self._rslvr._path_base}.{name}"
        )
        doc_val = on_off(self._rslvr.from_doc_dflts(doc_path, True))
        if doc_val is True:
            return doc_val
        return on_off(tbl_val) ^ on_off(para_val) ^ on_off(char_val)
