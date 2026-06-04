from functools import cached_property
from typing import Any, Literal

# docxray stuff
from docxray.oxml.trans.h2d.exceptions import DisplayError
from docxray.oxml.trans.proxy.compute import on_off
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    CharacterStyle,
)
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.text.run import Run
from docxray.oxml.trans.st.enums import (
    SE_UNDERLINE,
    SE_OnOff1,
    SE_StyleType,
    SE_VerticalAlignRun,
)

from .how2display import How2Display

type _OnOff = NotFound | bool | SE_OnOff1 | None
type CharsCase = Literal["up", "down"]


class RunH2D(How2Display[Run]):
    @cached_property
    def italic(self) -> bool:
        return self._display_val_toggled("i", "iCs")

    @cached_property
    def bold(self) -> bool:
        return self._display_val_toggled("b", "bCs")

    @cached_property
    def chars_case(self) -> CharsCase | None:
        if self._all_uppercase and self._all_downcase:
            raise DisplayError(
                "Mentiond 2 cases (up, down) when they are mutually exclusive"
            )
        if self._all_uppercase:
            return "up"
        if self._all_downcase:
            return "down"
        return None

    # TODO: double strike needed
    @cached_property
    def single_strike_through(self) -> bool:
        return self._display_val_toggled("strike")

    # TODO: change after if needed
    @cached_property
    def underline(self) -> None | SE_UNDERLINE:
        line = self._display_val("u")
        if isinstance(line, NotFound) or line == SE_UNDERLINE.NONE:
            return None
        if line is None:
            return SE_UNDERLINE.SINGLE
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

    @cached_property
    def cell(self) -> Cell | None:
        return self._proxy.paragraph.h2d.cell

    @cached_property
    def _all_uppercase(self) -> bool:
        return self._display_val_toggled("caps")

    @cached_property
    def _all_downcase(self) -> bool:
        return self._display_val_toggled("smallCaps")

    @cached_property
    def _char_style(self) -> CharacterStyle | None:
        style_id = self._prop_val("rStyle")
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.CHARACTER,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.CHARACTER],
        )

    def _display_val(self, name: str, optional: bool = True) -> Any:
        char_val = self._prop_val(name, optional, "both")
        if not isinstance(char_val, NotFound):
            return char_val
        para_val = self._proxy.paragraph.h2d._prop_val_run(name, optional)
        if not isinstance(para_val, NotFound):
            return para_val
        char_path = self._prop_path("val", f"{self._path_base}.{name}")
        cell = self.cell
        if cell:
            tbl_val, _ = self._from_tbl_style_hierarchy(
                cell.h2d._tbl_style_props_deep, char_path, optional
            )
            if not isinstance(tbl_val, NotFound):
                return tbl_val
        return self._from_doc_dflts(
            char_path.join_left("rPrDefault"), optional
        )

    def _display_val_toggled(self, name: str, cs: str | None = None) -> bool:
        char_direct_val = self._prop_val(name, True)
        if not isinstance(char_direct_val, NotFound):
            return on_off(char_direct_val)
        if cs:
            char_direct_val_cs = self._prop_val(cs)
            if not isinstance(char_direct_val, NotFound):
                return on_off(char_direct_val_cs)
        char_val = self._prop_val(name, True, "style")
        if cs and isinstance(char_val, NotFound):
            char_val = self._prop_val(cs, True, "style")
        para_val = self._proxy.paragraph.h2d._prop_val_run(name)
        if cs and isinstance(para_val, NotFound):
            para_val = self._proxy.paragraph.h2d._prop_val_run(cs)
        char_path = self._prop_path("val", f"{self._path_base}.{name}")
        tbl_val = NotFound(self, char_path)
        cell = self.cell
        char_path_cs = None
        if cell:
            tbl_val, _ = self._from_tbl_style_hierarchy(
                cell.h2d._tbl_style_props_deep, char_path, True
            )
            if cs and isinstance(tbl_val, NotFound):
                char_path_cs = self._prop_path(
                    "val", f"{self._path_base}.{cs}"
                )
                tbl_val, _ = self._from_tbl_style_hierarchy(
                    cell.h2d._tbl_style_props_deep, char_path_cs, True
                )
        found_count = sum(
            1
            for i in [char_val, para_val, tbl_val]
            if not isinstance(i, NotFound)
        )
        if found_count > 1:
            return self._effective_toggled(
                char_path, char_val, para_val, tbl_val, char_path_cs
            )
        if not isinstance(char_val, NotFound):
            return on_off(char_val)
        if not isinstance(para_val, NotFound):
            return on_off(para_val)
        if not isinstance(tbl_val, NotFound):
            return on_off(tbl_val)
        return False

    def _effective_toggled(
        self,
        char_path: PropertyPath,
        char_val: _OnOff,
        para_val: _OnOff,
        tbl_val: _OnOff,
        char_path_cs: PropertyPath | None = None,
    ) -> bool:
        doc_val = on_off(
            self._from_doc_dflts(char_path.join_left("rPrDefault"), True)
        )
        if doc_val is True:
            return doc_val
        elif char_path_cs:
            doc_val = on_off(
                self._from_doc_dflts(
                    char_path_cs.join_left("rPrDefault"), True
                )
            )
            if doc_val is True:
                return doc_val
        return on_off(tbl_val) ^ on_off(para_val) ^ on_off(char_val)

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self._char_style is None:
            return NotFound(self, path)
        return self._from_style_inheritance(self._char_style, path, optional)
