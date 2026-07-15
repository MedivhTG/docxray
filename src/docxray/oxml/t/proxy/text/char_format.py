from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, TypedDict, cast

# docxray stuff
from docxray.colorize import Colorize
from docxray.length import Length
from docxray.oxml.t.proxy.base import (
    NotFound,
    from_doc_dflts,
    from_style_inheritance,
)
from docxray.oxml.t.proxy.compute import (
    hps_measure,
    on_off,
    signed_hps_measure,
    signed_twips_measure,
    text_scale,
)
from docxray.oxml.t.proxy.exceptions import DisplayError
from docxray.oxml.t.proxy.text.font import Font
from docxray.oxml.t.proxy.text.language import Language
from docxray.oxml.t.st.enums import (
    SE_HEX_COLOR_AUTO,
    SE_HIGHLIGHT_COLOR,
    SE_THEME_COLOR,
    SE_UNDERLINE,
    SE_VERTICAL_ALIGN_RUN,
)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.numbering.numbering import Level

    from .run import Run

type CharsCase = Literal["caps", "small_caps"]
type StrikeCase = Literal["single", "double"]


class UnderlineInfo(TypedDict):
    line: SE_UNDERLINE
    color: str


class CharacterFormat:
    def __init__(self, char_proxy: Run | Level) -> None:
        from .run import Run

        self._proxy = char_proxy
        self._display = (
            self._display_run
            if isinstance(char_proxy, Run)
            else self._display_level
        )
        self._display_toggled = (
            self._display_run_toggled
            if isinstance(char_proxy, Run)
            else self._display_level_toggled
        )

    @cached_property
    def italic(self) -> bool:
        """Used italic bold-decoration."""
        if self._complex_script:
            return self._iCs
        return self._i

    @cached_property
    def bold(self) -> bool:
        """Used text bold-decoration."""
        if self._complex_script:
            return self._bCs
        return self._b

    @cached_property
    def font_size(self) -> Length | None:
        """Size of characters font."""
        if self._complex_script:
            return self._szCs
        return self._sz

    @cached_property
    def chars_case(self) -> CharsCase | None:
        """Used text transformation such as caps or font-variant as small-caps."""
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
        """Used single or double strike for text, not both."""
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
    def underline_info(self) -> UnderlineInfo | None:
        """Underline with info about line type and used color."""
        if self._u_line is None:
            return None
        return {
            "line": self._u_line,
            "color": Colorize.colorize(
                self._u_color or SE_HEX_COLOR_AUTO.AUTO,
                self._u_theme_color,
                self._proxy.document_part.theme.palette,
                self._u_theme_tint,
                self._u_theme_shade,
                prefer_theme=True,
            ),
        }

    @cached_property
    def vertical_alignment(self) -> SE_VERTICAL_ALIGN_RUN | None:
        """Vertical alignment for text - superscript, subscript."""
        align = self._display("rPr.vertAlign.val", False)
        if (
            isinstance(align, NotFound)
            or align == SE_VERTICAL_ALIGN_RUN.BASELINE
        ):
            return None
        return align

    @cached_property
    def font(self) -> Font | None:
        """Used font for text."""
        rFonts_elm = self._display("rPr.rFonts")
        if isinstance(rFonts_elm, NotFound):
            return None
        return Font(rFonts_elm, self._proxy)

    @cached_property
    def language(self) -> Language | None:
        """Used langugage for text."""
        lang_elm = self._display("rPr.lang")
        if isinstance(lang_elm, NotFound):
            return None
        return Language(lang_elm, self._proxy)

    @cached_property
    def right_to_left(self) -> bool:
        """Spelling for text is right-to-left."""
        return on_off(self._display("rPr.rtl.val", True))

    @cached_property
    def color(self) -> str:
        """Hexaadecimal color-presentation of an run text, e.g. `#000000` for black."""
        return Colorize.colorize(
            self._color or SE_HEX_COLOR_AUTO.AUTO,
            self._theme_color,
            self._proxy.document_part.theme.palette,
            self._theme_tint,
            self._theme_shade,
            prefer_theme=True,
        )

    @cached_property
    def highlight(self) -> SE_HIGHLIGHT_COLOR | None:
        highlight = self._display("rPr.highlight.val")
        if isinstance(highlight, NotFound) or highlight == "none":
            return None
        return highlight

    @cached_property
    def hide_text(self) -> bool:
        """Render text as hidden and free display space."""
        return self._display_toggled("rPr.vanish.val")

    @cached_property
    def text_scale(self) -> int:
        scale = self._display("rPr.w.val")
        if isinstance(scale, NotFound):
            return 100
        return text_scale(scale)

    @cached_property
    def letter_spacing(self) -> Length | None:
        spacing = self._display("rPr.spacing.val")
        if isinstance(spacing, NotFound):
            return None
        return signed_twips_measure(spacing)

    @cached_property
    def vertical_offset(self) -> Length | None:
        pos = self._display("rPr.position.val")
        if isinstance(pos, NotFound):
            return None
        return signed_hps_measure(pos)

    @cached_property
    def font_kerning(self) -> Length | None:
        kern = self._display("rPr.kern.val")
        if isinstance(kern, NotFound):
            return None
        return hps_measure(kern)

    @cached_property
    def _sz(self) -> Length | None:
        size = self._display("rPr.sz.val")
        if isinstance(size, NotFound):
            return None
        return hps_measure(size)

    @cached_property
    def _szCs(self) -> Length | None:
        size = self._display("rPr.szCs.val")
        if isinstance(size, NotFound):
            return None
        return hps_measure(size)

    @cached_property
    def _i(self) -> bool:
        return self._display_toggled("rPr.i.val")

    @cached_property
    def _iCs(self) -> bool:
        return self._display_toggled("rPr.iCs.val")

    @cached_property
    def _b(self) -> bool:
        return self._display_toggled("rPr.b.val")

    @cached_property
    def _bCs(self) -> bool:
        return self._display_toggled("rPr.bCs.val")

    @cached_property
    def _complex_script(self) -> bool:
        """Spelling for text is complex (has arabic, chinese, etc. chars)."""
        return on_off(self._display("rPr.cs.val", True))

    @cached_property
    def _caps(self) -> bool:
        return self._display_toggled("rPr.caps.val")

    @cached_property
    def _small_caps(self) -> bool:
        return self._display_toggled("rPr.smallCaps.val")

    @cached_property
    def _single_strike(self) -> bool:
        return self._display_toggled("rPr.strike.val")

    @cached_property
    def _double_strike(self) -> bool:
        return on_off(self._display("rPr.dstrike.val", True))

    @cached_property
    def _u_line(self) -> SE_UNDERLINE | None:
        line = self._display("rPr.u.val", True)
        if isinstance(line, NotFound) or line == SE_UNDERLINE.NONE:
            return None
        if line is None:
            return SE_UNDERLINE.SINGLE
        return line

    @cached_property
    def _u_color(self) -> SE_HEX_COLOR_AUTO | bytes | None:
        color = self._display("rPr.u.color")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _u_theme_color(self) -> SE_THEME_COLOR | None:
        color = self._display("rPr.u.themeColor")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _u_theme_tint(self) -> bytes | None:
        tint = self._display("rPr.u.themeTint")
        if isinstance(tint, NotFound):
            return None
        return tint

    @cached_property
    def _u_theme_shade(self) -> bytes | None:
        shade = self._display("rPr.u.themeShade")
        if isinstance(shade, NotFound):
            return None
        return shade

    @cached_property
    def _color(self) -> SE_HEX_COLOR_AUTO | bytes | None:
        color = self._display("rPr.color.val")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _theme_color(self) -> SE_THEME_COLOR | None:
        color = self._display("rPr.color.themeColor")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _theme_tint(self) -> bytes | None:
        tint = self._display("rPr.color.themeTint")
        if isinstance(tint, NotFound):
            return None
        return tint

    @cached_property
    def _theme_shade(self) -> bytes | None:
        shade = self._display("rPr.color.themeShade")
        if isinstance(shade, NotFound):
            return None
        return shade

    def _display_level(self, path: str, optional: bool = False) -> Any:
        prop = self._proxy.prop(path, optional)
        if isinstance(prop, NotFound):
            return from_doc_dflts(self._proxy, path, optional)
        return prop

    def _display_level_toggled(self, path: str) -> bool:
        return on_off(self._display_level(path, True))

    def _display_run(self, path: str, optional: bool = False) -> Any:
        run = cast("Run", self._proxy)
        char_val = self._prop_run(path, optional, "both")
        if not isinstance(char_val, NotFound):
            return char_val
        para_val = run.paragraph._prop(path, optional, "paragraph-style")
        if not isinstance(para_val, NotFound):
            return para_val
        tbl_val = run.paragraph._prop(path, optional, "table-style")
        if not isinstance(tbl_val, NotFound):
            return tbl_val
        return from_doc_dflts(run, f"rPrDefault.{path}", optional)

    def _display_run_toggled(self, path: str) -> bool:
        run = cast("Run", self._proxy)
        direct_val = self._prop_run(path, True)
        if not isinstance(direct_val, NotFound):
            return on_off(direct_val)
        char_val = self._prop_run(path, True, "style")
        para_val = run.paragraph._prop(path, True, "paragraph-style")
        tbl_val = run.paragraph._prop(path, True, "table-style")
        found_count = sum(
            1
            for i in [char_val, para_val, tbl_val]
            if not isinstance(i, NotFound)
        )
        if found_count > 1:
            doc_val = on_off(
                from_doc_dflts(self._proxy, f"rPrDefault.{path}", True)
            )
            if doc_val is True:
                return doc_val
            return on_off(tbl_val) ^ on_off(para_val) ^ on_off(char_val)
        if not isinstance(char_val, NotFound):
            return on_off(char_val)
        if not isinstance(para_val, NotFound):
            return on_off(para_val)
        if not isinstance(tbl_val, NotFound):
            return on_off(tbl_val)
        return False

    def _prop_run_direct(self, path: str, optional: bool = False) -> Any:
        return self._proxy.prop(path, optional)

    def _prop_run_style(self, path: str, optional: bool = False) -> Any:
        run = cast("Run", self._proxy)
        if run.character_style:
            return from_style_inheritance(
                run, run.character_style, path, optional
            )
        return NotFound(self, path)

    def _prop_run(
        self,
        path: str,
        optional: bool = False,
        where: Literal["direct", "style", "both"] = "direct",
    ) -> Any:
        if where == "direct":
            return self._prop_run_direct(path, optional)
        elif where == "style":
            return self._prop_run_style(path, optional)
        direct_val = self._prop_run_direct(path, optional)
        if isinstance(direct_val, NotFound):
            return self._prop_run_style(path, optional)
        return direct_val
