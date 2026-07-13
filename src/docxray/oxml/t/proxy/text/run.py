from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, TypedDict, cast

# docxray stuff
from docxray.colorize import Colorize
from docxray.oxml.t.proxy.base import (
    NotFound,
    StoryChild,
    from_doc_dflts,
    from_style_inheritance,
)
from docxray.oxml.t.proxy.compute import on_off
from docxray.oxml.t.proxy.exceptions import DisplayError
from docxray.oxml.t.proxy.styles.style import CharacterStyle
from docxray.oxml.t.st.enums import (
    SE_HEX_COLOR_AUTO,
    SE_STYLE_TYPE,
    SE_THEME_COLOR,
    SE_UNDERLINE,
    SE_VERTICAL_ALIGN_RUN,
)
from docxray.oxml.t.text.run import CT_R

from .font import Font
from .language import Language
from .run_content import RunInnerContent, TxtFragment, run_inner_content

if TYPE_CHECKING:
    from .paragraph import Paragraph

type CharsCase = Literal["caps", "small_caps"]
type StrikeCase = Literal["single", "double"]


class UnderlineInfo(TypedDict):
    line: SE_UNDERLINE
    color: str


class Run(StoryChild[CT_R]):
    @cached_property
    def paragraph(self) -> Paragraph:
        """Current paragraph where is run contained"""
        from .hyperlink import Hyperlink
        from .paragraph import Paragraph

        if isinstance(self._parent, Paragraph):
            return self._parent
        elif isinstance(self._parent, Hyperlink):
            return self._parent.paragraph
        return cast(Paragraph, self._parent)

    @cached_property
    def italic(self) -> bool:
        """Used italic bold-decoration."""
        return self._display_toggled("rPr.i.val")

    @cached_property
    def bold(self) -> bool:
        """Used text bold-decoration."""
        return self._display_toggled("rPr.b.val")

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
                self.document_part.theme.palette,
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
        return Font(rFonts_elm, self)

    @cached_property
    def language(self) -> Language | None:
        """Used langugage for text."""
        lang_elm = self._display("rPr.lang")
        if isinstance(lang_elm, NotFound):
            return None
        return Language(lang_elm, self)

    @cached_property
    def is_complex_script(self) -> bool:
        """Spelling for text is complex (has arabic, chinese, etc. chars)."""
        return on_off(self._display("rPr.cs.val", True))

    @cached_property
    def right_to_left(self) -> bool:
        """Spelling for text is right-to-left."""
        return on_off(self._display("rPr.rtl.val", True))

    @cached_property
    def raw_text(self) -> str:
        """Accumulated text from tags `<w:t>`."""
        txt = ""
        for item in self.iter_inner_content():
            if isinstance(item, TxtFragment):
                txt += item.raw
        return txt

    @cached_property
    def character_style(self) -> CharacterStyle | None:
        """Direct style applied for run."""
        style_id = self._prop("rPr.rStyle.val")
        if isinstance(style_id, NotFound):
            return None
        return self.document_part.styles.get_by_id(
            style_id, SE_STYLE_TYPE.CHARACTER, CharacterStyle
        )

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

    def _display(self, path: str, optional: bool = False) -> Any:
        char_val = self._prop(path, optional, "both")
        if not isinstance(char_val, NotFound):
            return char_val
        para_val = self.paragraph._prop(path, optional, "paragraph-style")
        if not isinstance(para_val, NotFound):
            return para_val
        tbl_val = self.paragraph._prop(path, optional, "table-style")
        if not isinstance(tbl_val, NotFound):
            return tbl_val
        return from_doc_dflts(self, f"rPrDefault.{path}", optional)

    def _display_toggled(self, path: str) -> bool:
        direct_val = self._prop(path, True)
        if not isinstance(direct_val, NotFound):
            return on_off(direct_val)
        char_val = self._prop(path, True, "style")
        para_val = self.paragraph._prop(path, True, "paragraph-style")
        tbl_val = self.paragraph._prop(path, True, "table-style")
        found_count = sum(
            1
            for i in [char_val, para_val, tbl_val]
            if not isinstance(i, NotFound)
        )
        if found_count > 1:
            doc_val = on_off(from_doc_dflts(self, f"rPrDefault.{path}", True))
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

    def _prop_direct(self, path: str, optional: bool = False) -> Any:
        return self.prop(path, optional)

    def _prop_style(self, path: str, optional: bool = False) -> Any:
        if self.character_style:
            return from_style_inheritance(
                self, self.character_style, path, optional
            )
        return NotFound(self, path)

    def _prop(
        self,
        path: str,
        optional: bool = False,
        where: Literal["direct", "style", "both"] = "direct",
    ) -> Any:
        if where == "direct":
            return self._prop_direct(path, optional)
        elif where == "style":
            return self._prop_style(path, optional)
        direct_val = self._prop_direct(path, optional)
        if isinstance(direct_val, NotFound):
            return self._prop_style(path, optional)
        return direct_val

    def iter_inner_content(
        self,
    ) -> Iterator[RunInnerContent]:
        for item in self.element.inner_content_items:
            yield run_inner_content(item, self)
