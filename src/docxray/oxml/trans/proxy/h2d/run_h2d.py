from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.compute import on_off
from docxray.oxml.trans.proxy.h2d.table_h2d import CellH2D
from docxray.oxml.trans.proxy.shared import NotFound

from .how_to_display import How2Display
from .run_rslv import RunResolver


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

    def _display_toggled(self, prop: str) -> bool:
        char_direct_val: bool | NotFound = getattr(self._rslvr, prop)
        if not isinstance(char_direct_val, NotFound):
            return char_direct_val

        char_path = self._rslvr._prop_path("val", f"rPr.{prop}")
        char_val: NotFound | bool = self._rslvr._from_styles_hierarchy(
            char_path, True
        )
        para_val: NotFound | bool = getattr(
            self._rslvr.paragraph_resolver, prop
        )
        tbl_val: NotFound | bool = NotFound(self, char_path)
        if self.cell_h2d:
            tbl_val = getattr(self.cell_h2d, f"_{prop}")
        found_vals_count = sum(
            1
            for item in [char_val, para_val, tbl_val]
            if isinstance(item, bool)
        )
        if found_vals_count > 1:
            return self._effective_toggled(prop, char_val, para_val, tbl_val)
        if not isinstance(char_val, NotFound):
            return char_val
        if not isinstance(para_val, NotFound):
            return para_val
        if not isinstance(tbl_val, NotFound):
            return tbl_val
        return False

    def _effective_toggled(
        self,
        prop: str,
        char_val: bool | NotFound,
        para_val: bool | NotFound,
        tbl_val: bool | NotFound,
    ) -> bool:
        doc_path = self._rslvr._prop_path(
            prop, f"rPrDefault.{self._rslvr._path_base}"
        )
        doc_val = on_off(self._rslvr._from_doc_dflts(doc_path))
        if doc_val is True:
            return doc_val
        return on_off(tbl_val) ^ on_off(para_val) ^ on_off(char_val)
