from functools import cached_property
from typing import Any, Literal, TypedDict

# docxray stuff
from docxray.colorize import Colorize
from docxray.oxml.t.h2d.exceptions import DisplayError
from docxray.oxml.t.proxy.compute import on_off
from docxray.oxml.t.proxy.base import NotFound, PropertyPath
from docxray.oxml.t.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    CharacterStyle,
)
from docxray.oxml.t.proxy.table.cell import Cell
from docxray.oxml.t.proxy.text.font import Font
from docxray.oxml.t.proxy.text.language import Language
from docxray.oxml.t.proxy.text.run import Run
from docxray.oxml.t.st.enums import (
    SE_HEX_COLOR_AUTO,
    SE_THEME_COLOR,
    SE_UNDERLINE,
    SE_ON_OFF_1,
    SE_STYLE_TYPE,
    SE_VERTICAL_ALIGN_RUN,
)

from .how2display import How2Display

type _OnOff = NotFound | bool | SE_ON_OFF_1 | None

type CharsCase = Literal["caps", "small_caps"]
type StrikeCase = Literal["single", "double"]


class UnderlineInfo(TypedDict):
    line: SE_UNDERLINE
    color: str


class RunH2D(How2Display[Run]):
    @cached_property
    def italic(self) -> bool:
        return self._display_val_toggled("i")

    @cached_property
    def bold(self) -> bool:
        return self._display_val_toggled("b")

    @cached_property
    def chars_case(self) -> CharsCase | None:
        if self._caps and self._small_caps:
            raise DisplayError(
                "Mentiond 2 cases (caps, small_caps) when they are mutually exclusive"
            )
        if self._caps:
            return "caps"
        if self._small_caps:
            return "small_caps"
        return None

    @cached_property
    def strike_case(self) -> StrikeCase | None:
        if self._single_strike and self._double_strike:
            raise DisplayError(
                "Mentiond 2 cases (single, double) when they are mutually exclusive"
            )
        if self._single_strike:
            return "single"
        if self._double_strike:
            return "double"
        return None

    @cached_property
    def underline(self) -> UnderlineInfo | None:
        line = self._display_val("u")
        if isinstance(line, NotFound) or line == SE_UNDERLINE.NONE:
            return None
        u: UnderlineInfo = {"line": line, "color": "#000000"}
        if line is None:
            u["line"] = SE_UNDERLINE.SINGLE

        theme_color_path = self._prop_path(
            "themeColor", f"{self._path_base}.u"
        )
        theme_color: SE_THEME_COLOR | None | NotFound = self._display(
            theme_color_path
        )
        if isinstance(theme_color, NotFound):
            theme_color = None
        theme_tint_path = self._prop_path("themeTint", f"{self._path_base}.u")
        theme_tint: bytes | NotFound | None = self._display(theme_tint_path)
        if isinstance(theme_tint, NotFound):
            theme_tint = None
        theme_shade_path = self._prop_path(
            "themeShade", f"{self._path_base}.u"
        )
        theme_shade: bytes | NotFound | None = self._display(theme_shade_path)
        if isinstance(theme_shade, NotFound):
            theme_shade = None
        color_path = self._prop_path("color", f"{self._path_base}.u")
        color: SE_HEX_COLOR_AUTO | bytes = self._display(color_path)
        u["color"] = Colorize.colorize(
            color,
            theme_color,
            self._document_part.theme.palette,
            theme_tint,
            theme_shade,
            prefer_theme=True,
        )
        return u

    @cached_property
    def vertical_alignment(self) -> None | SE_VERTICAL_ALIGN_RUN:
        align = self._display_val("vertAlign", False)
        if (
            isinstance(align, NotFound)
            or align == SE_VERTICAL_ALIGN_RUN.BASELINE
        ):
            return None
        return align

    @cached_property
    def font(self) -> Font | None:
        rFonts_elm = self._display_val("rFonts")
        if isinstance(rFonts_elm, NotFound):
            return None
        return Font(rFonts_elm, self._proxy)

    @cached_property
    def language(self) -> Language | None:
        lang_elm = self._display_val("lang", False)
        if isinstance(lang_elm, NotFound):
            return None
        return Language(lang_elm, self._proxy)

    @cached_property
    def is_complex_script(self) -> bool:
        return on_off(self._display_val("cs"))

    @cached_property
    def right_to_left(self) -> bool:
        return on_off(self._display_val("rtl"))

    @cached_property
    def cell(self) -> Cell | None:
        return self._proxy.paragraph.h2d.cell

    @cached_property
    def _caps(self) -> bool:
        return self._display_val_toggled("caps")

    @cached_property
    def _small_caps(self) -> bool:
        return self._display_val_toggled("smallCaps")

    @cached_property
    def _single_strike(self) -> bool:
        return self._display_val_toggled("strike")

    @cached_property
    def _double_strike(self) -> bool:
        return on_off(self._display_val("dstrike"))

    @cached_property
    def _char_style(self) -> CharacterStyle | None:
        style_id = self._prop_val("rStyle")
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_STYLE_TYPE.CHARACTER,
            S_TYPE_TO_STYLE_CLS[SE_STYLE_TYPE.CHARACTER],
        )

    def _display(
        self, name_or_path: str | PropertyPath, optional: bool = False
    ) -> Any:
        char_val = self._prop(name_or_path, optional, "both")
        if not isinstance(char_val, NotFound):
            return char_val
        para_val = self._proxy.paragraph.h2d._prop_run(name_or_path, optional)
        if not isinstance(para_val, NotFound):
            return para_val
        if isinstance(name_or_path, PropertyPath):
            char_path = name_or_path
        else:
            char_path = self._prop_path(name_or_path, self._path_base)
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

    def _display_val_toggled(self, name: str) -> bool:
        char_direct_val = self._prop_val(name, True)
        if not isinstance(char_direct_val, NotFound):
            return on_off(char_direct_val)
        char_val = self._prop_val(name, True, "style")
        para_val = self._proxy.paragraph.h2d._prop_val_run(name)
        char_path = self._prop_path("val", f"{self._path_base}.{name}")
        tbl_val = NotFound(self, char_path)
        cell = self.cell
        if cell:
            tbl_val, _ = self._from_tbl_style_hierarchy(
                cell.h2d._tbl_style_props_deep, char_path, True
            )
        found_count = sum(
            1
            for i in [char_val, para_val, tbl_val]
            if not isinstance(i, NotFound)
        )
        if found_count > 1:
            return self._effective_toggled(
                char_path, char_val, para_val, tbl_val
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
    ) -> bool:
        doc_val = on_off(
            self._from_doc_dflts(char_path.join_left("rPrDefault"), True)
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
