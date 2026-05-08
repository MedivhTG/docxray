from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.shared import PropertyPath

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
        if self._rslvr.para_style:
            para_val = bool(
                self._rslvr._from_style_inheritance(
                    self._rslvr.para_style, prop_path
                )
            )
        return para_val ^ char_val
