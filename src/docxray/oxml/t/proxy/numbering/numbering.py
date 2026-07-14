from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.colorize import Colorize
from docxray.length import Length
from docxray.oxml.t.exceptions import InvalidXmlError
from docxray.oxml.t.numbering import (
    CT_AbstractNum,
    CT_Lvl,
    CT_Num,
    CT_Numbering,
    CT_NumLvl,
)
from docxray.oxml.t.proxy.base import ElementProxy, NotFound, from_doc_dflts
from docxray.oxml.t.proxy.compute import hps_measure, on_off
from docxray.oxml.t.proxy.exceptions import DisplayError
from docxray.oxml.t.proxy.styles.style import (
    NumberingStyle,
    ParagraphStyle,
)
from docxray.oxml.t.proxy.styles.styles import Styles
from docxray.oxml.t.proxy.text.font import Font
from docxray.oxml.t.proxy.text.language import Language
from docxray.oxml.t.proxy.text.run import CharsCase, StrikeCase, UnderlineInfo
from docxray.oxml.t.proxy.types import ProvidesXmlPart
from docxray.oxml.t.st.enums import (
    SE_HEX_COLOR_AUTO,
    SE_HIGHLIGHT_COLOR,
    SE_JC,
    SE_LEVEL_SUFFIX,
    SE_NUMBER_FORMAT,
    SE_STYLE_TYPE,
    SE_THEME_COLOR,
    SE_UNDERLINE,
    SE_VERTICAL_ALIGN_RUN,
)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.parts.numbering import NumberingPart


class Level(ElementProxy[CT_Lvl]):
    @cached_property
    def paragraph_style(self) -> ParagraphStyle | None:
        """Paragraph style linked to level itself.

        If here is pStyle element inside, but referenced paragraph
        style has numPr element, than `None` returned instead
        (numbering cannot related to para style with back ref).

        Returns:
            ParagraphStyle | None: Paragraph style or None of not exist (or other case).
        """
        pStyle_elm = self.element.pStyle
        if pStyle_elm is None:
            return None
        style = self.parent.numbering.styles.get_by_id(
            pStyle_elm.val, SE_STYLE_TYPE.PARAGRAPH, ParagraphStyle
        )
        pPr_elm = style.element.pPr
        if pPr_elm is not None:
            if pPr_elm.numPr is not None:
                return None
        return style

    @cached_property
    def parent(self) -> AbstractNum | LevelOverride:
        return cast("AbstractNum | LevelOverride", self._parent)

    @cached_property
    def ilvl(self) -> int:
        return self._element.ilvl

    @cached_property
    def alignment(self) -> SE_JC:
        if self._element.lvlJc is None:
            return SE_JC.LEFT
        return self._element.lvlJc.val

    @cached_property
    def separator(self) -> SE_LEVEL_SUFFIX:
        if self._element.suff is None:
            return SE_LEVEL_SUFFIX.TAB
        return self._element.suff.val

    @cached_property
    def start_from(self) -> int:
        if isinstance(self.parent, LevelOverride):
            start = self.parent.start_from
            if start is not None:
                return start
        if self.element.start is None:
            return 0
        return self.element.start.val

    @cached_property
    def numbering_format(self) -> SE_NUMBER_FORMAT:
        if self.element.numFmt is None:
            return SE_NUMBER_FORMAT.DECIMAL
        return self.element.numFmt.val

    @cached_property
    def numbering_custom_pattern(self) -> str:
        if self.element.numFmt is None:
            return ""
        return self.element.numFmt.format or ""

    @cached_property
    def pattern(self) -> str:
        if self.element.lvlText is None:
            return ""
        pattern = self.element.lvlText.val
        if pattern is None:
            if on_off(self.element.lvlText.null):
                return "\0"
            return ""
        return pattern

    @cached_property
    def restart_from(self) -> int | None:
        if self.element.lvlRestart is None:
            return None
        return self.element.lvlRestart.val

    @cached_property
    def all_decimal(self) -> bool:
        return (
            False if self.element.isLgl is None else on_off(self.element.isLgl)
        )

    @cached_property
    def font(self) -> Font | None:
        rFonts_elm = self._display("rPr.rFonts")
        if isinstance(rFonts_elm, NotFound):
            return None
        return Font(rFonts_elm, self)

    @cached_property
    def language(self) -> Language | None:
        lang_elm = self._display("rPr.lang")
        if isinstance(lang_elm, NotFound):
            return None
        return Language(lang_elm, self)

    @cached_property
    def right_to_left(self) -> bool:
        return on_off(self._display("rPr.rtl.val", True))

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
    def underline_info(self) -> UnderlineInfo | None:
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
    def vertical_alignment(self) -> None | SE_VERTICAL_ALIGN_RUN:
        valign = self._display("rPr.vertAlign.val")
        if (
            isinstance(valign, NotFound)
            or valign == SE_VERTICAL_ALIGN_RUN.BASELINE
        ):
            return None
        return valign

    @cached_property
    def color(self) -> str:
        """Hexaadecimal color-presentation of an run text, e.g. `#000000` for black."""
        return Colorize.colorize(
            self._color or SE_HEX_COLOR_AUTO.AUTO,
            self._theme_color,
            self.document_part.theme.palette,
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
    def _complex_script(self) -> bool:
        return on_off(self._display("rPr.cs.val", True))

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
        return on_off(self._display("rPr.i.val", True))

    @cached_property
    def _iCs(self) -> bool:
        return on_off(self._display("rPr.iCs.val", True))

    @cached_property
    def _b(self) -> bool:
        return on_off(self._display("rPr.b.val", True))

    @cached_property
    def _bCs(self) -> bool:
        return on_off(self._display("rPr.bCs.val", True))

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

    @cached_property
    def _caps(self) -> bool:
        return on_off(self._display("rPr.caps.val", True))

    @cached_property
    def _small_caps(self) -> bool:
        return on_off(self._display("rPr.smallCaps.val", True))

    @cached_property
    def _single_strike(self) -> bool:
        return on_off(self._display("rPr.strike.val", True))

    @cached_property
    def _double_strike(self) -> bool:
        return on_off(self._display("rPr.dstrike.val", True))

    def _display(self, path: str, optional: bool = False) -> Any:
        prop = self.prop(path, optional)
        if isinstance(prop, NotFound):
            return from_doc_dflts(self, path, optional)
        return prop


class LevelOverride(ElementProxy[CT_NumLvl]):
    @cached_property
    def num(self) -> Num:
        return cast("Num", self._parent)

    @cached_property
    def numbering(self) -> Numbering:
        return self.num.numbering

    @cached_property
    def start_from(self) -> int | None:
        startOverride_elm = self.element.startOverride
        if startOverride_elm is None:
            return None
        return startOverride_elm.val

    @cached_property
    def lvl(self) -> Level | None:
        lvl_elm = self.element.lvl
        if lvl_elm is None:
            return None
        return Level(lvl_elm, self)


class AbstractNum(ElementProxy[CT_AbstractNum]):
    def __init__(
        self, element: CT_AbstractNum, parent: ProvidesXmlPart
    ) -> None:
        super().__init__(element, parent)
        self._cached_lvls: dict[int, Level] = {}

    @cached_property
    def numbering(self) -> Numbering:
        return cast("Numbering", self._parent)

    @cached_property
    def numbering_style(self) -> NumberingStyle | None:
        """This style is `not None` if abstract numbering
        do not contains info about properties of list items and
        those properties must be resolved from style hierarchy
        and back referenced numbering definitions.
        """
        style_id = self.element.numStyleLink
        if style_id is None:
            return None
        return self.numbering.styles.get_by_id(
            style_id.val, SE_STYLE_TYPE.NUMBERING, NumberingStyle
        )

    def lvl_by_ilvl(self, ilvl: int) -> Level:
        if lvl := self._cached_lvls.get(ilvl):
            return lvl
        lvl_elm = self.element.lvl_by_ilvl(ilvl)
        if lvl_elm is None:
            msg = f"No associated level for {ilvl}"
            raise InvalidXmlError(msg)
        lvl = Level(lvl_elm, self)
        self._cached_lvls[ilvl] = lvl
        return lvl

    def lvl_by_para_style(self, style_id: str) -> Level:
        for lvl in self._cached_lvls.values():
            pStyle_elm = lvl.element.pStyle
            if pStyle_elm is not None and pStyle_elm.val == style_id:
                return lvl
        lvl_elm = self.element.lvl_by_para_style(style_id)
        if lvl_elm is None:
            msg = f"No associated level for {style_id}"
            raise InvalidXmlError(msg)
        lvl = Level(lvl_elm, self)
        self._cached_lvls[lvl_elm.ilvl] = lvl
        return lvl


class Num(ElementProxy[CT_Num]):
    def __init__(self, element: CT_Num, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_lvl_overrides: dict[int, LevelOverride] = {}

    @cached_property
    def numbering(self) -> Numbering:
        return cast("Numbering", self._parent)

    @cached_property
    def abstract_num(self) -> AbstractNum:
        return self.numbering.get_abstract_num(self.element.abstractNumId.val)

    def associated_lvl_override(self, ilvl: int) -> LevelOverride | None:
        if lvl_override := self._cached_lvl_overrides.get(ilvl):
            return lvl_override
        overrideLvl_elm = self.element.override_num_by_ilvl(ilvl)
        if overrideLvl_elm is None:
            return None
        lvl_override = LevelOverride(overrideLvl_elm, self)
        self._cached_lvl_overrides[ilvl] = lvl_override
        return lvl_override


class Numbering(ElementProxy[CT_Numbering]):
    def __init__(self, element: CT_Numbering, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_nums: dict[int, Num] = {}
        self._cached_abstract_nums: dict[int, AbstractNum] = {}

    @cached_property
    def part(self) -> NumberingPart:
        return cast("NumberingPart", self._parent)

    @cached_property
    def styles(self) -> Styles:
        return self.part.styles

    def get_num(self, num_id: int) -> Num:
        if num := self._cached_nums.get(num_id):
            return num
        num_elm = self.element.num_by_id(num_id)
        if num_elm is None:
            msg = f"Referenced num with `{num_id}` not found"
            raise InvalidXmlError(msg)
        num = Num(num_elm, self)
        self._cached_nums[num_id] = num
        return num

    def get_abstract_num(self, abstract_num_id: int) -> AbstractNum:
        if abstract_num := self._cached_abstract_nums.get(abstract_num_id):
            return abstract_num
        abstractNum_elm = self.element.abstract_num_by_id(abstract_num_id)
        if abstractNum_elm is None:
            msg = "Referenced abstract num not found"
            raise InvalidXmlError(msg)
        abstract_num = AbstractNum(abstractNum_elm, self)
        self._cached_abstract_nums[abstract_num_id] = abstract_num
        return abstract_num

    def find_effective_num(self, num_id: int) -> Num:
        num = self.get_num(num_id)
        abstract_num = num.abstract_num
        num_style = abstract_num.numbering_style
        # Real abstract num can be hidden in deep inheritance
        while num_style:
            num = num_style.num
            abstract_num = num.abstract_num
            num_style = abstract_num.numbering_style
        return num

    # TODO: if no lvl but override exists - need to get props from it
    def associated_level(
        self, num_id: int, ilvl_or_style_id: int | str
    ) -> Level:
        num = self.find_effective_num(num_id)
        if isinstance(ilvl_or_style_id, int):
            num_init = self.get_num(num_id)
            override = num_init.associated_lvl_override(ilvl_or_style_id)
            if override and override.lvl:
                return override.lvl
            return num.abstract_num.lvl_by_ilvl(ilvl_or_style_id)
        return num.abstract_num.lvl_by_para_style(ilvl_or_style_id)
