from __future__ import annotations

from collections.abc import Callable
from enum import StrEnum
from functools import cached_property, lru_cache
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.oxml.trans.proxy.shared import ElementProxy, NotFound
from docxray.oxml.trans.proxy.text.language import Language
from docxray.oxml.trans.shared import CT_Fonts
from docxray.oxml.trans.st.enums import SE_HINT

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.numbering.numbering import Level
    from docxray.oxml.trans.proxy.text.run import Run


class FontSlot(StrEnum):
    ASCII = "ascii"
    HIGH_ANSI = "hAnsi"
    EAST_ASIA = "eastAsia"
    COMPLEX_SCRIPT = "cs"


def u_set(start: int, end: int) -> set[int]:
    return set(range(start, end + 1))


def in_encoding(char: str, encoding: str) -> bool:
    try:
        char.encode(encoding)
        return True
    except UnicodeEncodeError:
        return False


_LATN_SUP_1_EAST_ASIA_EXC = (
    {0x00A1, 0x00A4, 0x00AA, 0x00AD, 0x00AF, 0x00D7, 0x00F7}
    | u_set(0x00A7, 0x00A8)
    | u_set(0x00B0, 0x00B4)
    | u_set(0x00B6, 0x00BA)
    | u_set(0x00BC, 0x00BF)
)
_LATN_SUP_1_EAST_ASIA_ZH_EXC = (
    u_set(0x00E0, 0x00E1)
    | u_set(0x00E8, 0x00EA)
    | u_set(0x00EC, 0x00ED)
    | u_set(0x00F2, 0x00F3)
    | u_set(0x00F9, 0x00FA)
    | {0x00FC}
)
_ALPHA_P_FORMS_EAST_ASIA_EXC = u_set(0xFB00, 0xFB1C)
_ALPHA_P_FORMS_ASCII_EXC = u_set(0xFB1D, 0xFB4F)


class Font(ElementProxy[CT_Fonts]):
    @cached_property
    def parent(self) -> "Level | Run":
        return cast("Level | Run", self._parent)

    @cached_property
    def _lang(self) -> Language | None:
        return self.parent.language

    @cached_property
    def _east_asia_lang(self) -> str | None:
        if self._lang:
            return self._lang.east_asia_slot
        return None

    @cached_property
    def _hint(self) -> SE_HINT | None:
        return self._prop_resolved("hint")

    @cached_property
    def _ascii(self) -> str | None:
        return self._prop_resolved("ascii")

    @cached_property
    def _hAnsi(self) -> str | None:
        return self._prop_resolved("hAnsi")

    @cached_property
    def _eastAsia(self) -> str | None:
        return self._prop_resolved("eastAsia")

    @cached_property
    def _cs(self) -> str | None:
        return self._prop_resolved("cs")

    # TODO: look for fonts inside of Theme (if present)
    @lru_cache
    def guess_font(self, char: str) -> str | None:
        """Guess single character font - which font slot must be used.

        If `None` returned then the text shall be displayed
        in any default font which supports these characters.

        Args:
            char (str): Character string

        Returns:
            str | None: Font-family or `None`.
        """
        slot = self._guess_slot(char)
        if slot == "ascii":
            return self._ascii
        if slot == "hAnsi":
            return self._hAnsi
        if slot == "eastAsia":
            return self._eastAsia
        return self._cs

    def _guess_slot(self, char: str) -> FontSlot:
        unicode = ord(char)
        for u_set, classificator in CLASS_TABLE:
            if unicode in u_set:
                if isinstance(classificator, FontSlot):
                    font_slot = classificator
                else:
                    font_slot = classificator(self, unicode)
                if font_slot == "eastAsia" and self._hint == "eastAsia":
                    return FontSlot.EAST_ASIA
                elif (
                    self.parent.is_complex_script or self.parent.right_to_left
                ):
                    return FontSlot.COMPLEX_SCRIPT
                else:
                    return font_slot
        raise ValueError(f"No font slot for given char `{char}`")

    def _prop_resolved(self, name: str) -> Any:
        # docxray stuff
        from docxray.oxml.trans.proxy.text.run import Run

        if isinstance(self.parent, Run):
            prop = self.parent.h2d._display_val(name, False)
            if isinstance(prop, NotFound):
                return None
        return getattr(self.element, name, None)

    def _latin_1_supplement_slot(self, unicode: int) -> FontSlot:
        if self._hint == "eastAsia":
            if unicode in _LATN_SUP_1_EAST_ASIA_EXC:
                return FontSlot.EAST_ASIA
            if (
                self._east_asia_lang == "zh"
                and unicode in _LATN_SUP_1_EAST_ASIA_ZH_EXC
            ):
                return FontSlot.EAST_ASIA
        return FontSlot.HIGH_ANSI

    def _high_ansi_or_east_asia_zh_chinese(self, unicode: int) -> FontSlot:
        if self._hint == "eastAsia":
            ch = chr(unicode)
            if (
                self._east_asia_lang == "zh"
                or in_encoding(ch, "big5")
                or in_encoding(ch, "gb2312")
            ):
                return FontSlot.EAST_ASIA
        return FontSlot.HIGH_ANSI

    def _high_ansi_or_east_asia(self, unicode: int) -> FontSlot:
        if self._hint == "eastAsia":
            return FontSlot.EAST_ASIA
        return FontSlot.HIGH_ANSI

    def _high_ansi_or_east_asia_zh(self, unicode: int) -> FontSlot:
        if self._hint == "eastAsia" and self._east_asia_lang == "zh":
            return FontSlot.EAST_ASIA
        return FontSlot.HIGH_ANSI

    def _alphabetic_presentation_forms(self, unicode: int) -> FontSlot:
        if self._hint == "eastAsia":
            if unicode in _ALPHA_P_FORMS_EAST_ASIA_EXC:
                return FontSlot.EAST_ASIA
            if unicode in _ALPHA_P_FORMS_ASCII_EXC:
                return FontSlot.ASCII
        return FontSlot.HIGH_ANSI


CLASS_TABLE: list[
    tuple[set[int], FontSlot | Callable[[Font, int], FontSlot]]
] = [
    # Basic Latin, Hebrew, Arabic, Syriac, Arabic Supplement, Thaana,
    # Arabic Presentation Forms-A, Arabic Presentation Forms-B
    (
        u_set(0x0000, 0x007F)
        | u_set(0x0590, 0x05FF)
        | u_set(0x0600, 0x06FF)
        | u_set(0x0700, 0x074F)
        | u_set(0x0750, 0x077F)
        | u_set(0x0780, 0x07BF)
        | u_set(0xFB50, 0xFDFF)
        | u_set(0xFE70, 0xFEFE),
        FontSlot.ASCII,
    ),
    # Latin-1 Supplement
    (u_set(0x00A0, 0x00FF), Font._latin_1_supplement_slot),
    # Latin Extended-A, Latin Extended-B, IPA Extensions
    (
        u_set(0x0100, 0x017F) | u_set(0x0180, 0x024F) | u_set(0x0250, 0x02AF),
        Font._high_ansi_or_east_asia_zh_chinese,
    ),
    # Spacing Modifier Letters, Combining Diacritical Marks, Greek, Cyrillic
    # General Punctuation, Superscripts and Subscripts, Currency Symbols,
    # Combining Diacritical Marks for Symbols, Letter-like Symbols, Number Forms
    # Arrows, Mathematical Operators, Miscellaneous Technical, Control Pictures,
    # Optical Character Recognition, Enclosed Alphanumerics, Box Drawing, Block Elements,
    # Geometric Shapes, Miscellaneous Symbols, Dingbats, Private Use Area
    (
        u_set(0x02B0, 0x02FF)
        | u_set(0x0300, 0x036F)
        | u_set(0x0370, 0x03CF)
        | u_set(0x0400, 0x04FF)
        | u_set(0x2000, 0x206F)
        | u_set(0x2070, 0x209F)
        | u_set(0x20A0, 0x20CF)
        | u_set(0x20D0, 0x20FF)
        | u_set(0x2100, 0x214F)
        | u_set(0x2150, 0x218F)
        | u_set(0x2190, 0x21FF)
        | u_set(0x2200, 0x22FF)
        | u_set(0x2300, 0x23FF)
        | u_set(0x2400, 0x243F)
        | u_set(0x2440, 0x245F)
        | u_set(0x2460, 0x24FF)
        | u_set(0x2500, 0x257F)
        | u_set(0x2580, 0x259F)
        | u_set(0x25A0, 0x25FF)
        | u_set(0x2600, 0x26FF)
        | u_set(0x2700, 0x27BF)
        | u_set(0xE000, 0xF8FF),
        Font._high_ansi_or_east_asia,
    ),
    # Hangul Jamo, CJK Radicals Supplement, Kangxi Radicals, Ideographic Description Characters,
    # CJK Symbols and Punctuation, Hiragana, Katakana, Bopomofo, Hangul Compatibility Jamo,
    # Kanbun, Enclosed CJK Letters and Months, CJK Compatibility, CJK Unified Ideographs Extension A,
    # CJK Unified Ideographs, Yi Syllables, Yi Radicals, Hangul Syllables, High Surrogates,
    # High Private Use Surrogates, Low Surrogates, CJK Compatibility Ideographs,
    # CJK Compatibility Forms, Small Form Variants, Halfwidth and Fullwidth Forms
    (
        u_set(0x1100, 0x11FF)
        | u_set(0x2E80, 0x2EFF)
        | u_set(0x2F00, 0x2FDF)
        | u_set(0x2FF0, 0x2FFF)
        | u_set(0x3000, 0x303F)
        | u_set(0x3040, 0x309F)
        | u_set(0x30A0, 0x30FF)
        | u_set(0x3100, 0x312F)
        | u_set(0x3130, 0x318F)
        | u_set(0x3190, 0x319F)
        | u_set(0x3200, 0x32FF)
        | u_set(0x3300, 0x33FF)
        | u_set(0x3400, 0x4DBF)
        | u_set(0x4E00, 0x9FAF)
        | u_set(0xA000, 0xA48F)
        | u_set(0xA490, 0xA4CF)
        | u_set(0xAC00, 0xD7AF)
        | u_set(0xD800, 0xDB7F)
        | u_set(0xDB80, 0xDBFF)
        | u_set(0xDC00, 0xDFFF)
        | u_set(0xF900, 0xFAFF)
        | u_set(0xFE30, 0xFE4F)
        | u_set(0xFE50, 0xFE6F)
        | u_set(0xFF00, 0xFFEF),
        FontSlot.EAST_ASIA,
    ),
    # Latin Extended Additional
    (u_set(0x1E00, 0x1EFF), Font._high_ansi_or_east_asia_zh),
    # Greek Extended
    (u_set(0x1F00, 0x1FFF), FontSlot.HIGH_ANSI),
    # Alphabetic Presentation Forms
    (u_set(0xFB00, 0xFB4F), Font._alphabetic_presentation_forms),
]
