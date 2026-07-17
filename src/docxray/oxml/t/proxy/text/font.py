from __future__ import annotations

from collections.abc import Callable
from enum import StrEnum
from functools import cached_property, lru_cache
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.oxml.t.proxy.base import ElementProxy, NotFound
from docxray.oxml.t.proxy.text.language import Language
from docxray.oxml.t.proxy.theme import FontFamily
from docxray.oxml.t.shared import CT_Fonts
from docxray.oxml.t.st.enums import SE_HINT, SE_THEME

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.numbering.numbering import Level
    from docxray.oxml.t.proxy.text.char_format import CharacterFormat
    from docxray.oxml.t.proxy.text.run import Run


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
    def _ch_fmt(self) -> CharacterFormat:
        return self.parent.character_format

    @cached_property
    def _lang(self) -> Language | None:
        return self._ch_fmt.language

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
    def _asciiTheme(self) -> FontFamily | None:
        return self._theme_font("asciiTheme")

    @cached_property
    def _hAnsi(self) -> str | None:
        return self._prop_resolved("hAnsi")

    @cached_property
    def _hAnsiTheme(self) -> FontFamily | None:
        return self._theme_font("hAnsiTheme")

    @cached_property
    def _eastAsia(self) -> str | None:
        return self._prop_resolved("eastAsia")

    @cached_property
    def _eastAsiaTheme(self) -> FontFamily | None:
        return self._theme_font("eastAsiaTheme")

    @cached_property
    def _cs(self) -> str | None:
        return self._prop_resolved("cs")

    @cached_property
    def _cstheme(self) -> FontFamily | None:
        return self._theme_font("cstheme")

    @lru_cache
    def guess_font(self, char: str, default: str = "Arial") -> str:
        """Guess single character font - which font slot must be used.

        Args:
            char (str): Character string.
            default (str, optional): Default font if can't guess current. Defaults to Arial.

        Returns:
            str: Font-family string.
        """
        slot = self._guess_slot(char)
        if slot == "ascii":
            font_family = self._ascii or self._asciiTheme
        elif slot == "hAnsi":
            font_family = self._hAnsi or self._hAnsiTheme
        elif slot == "eastAsia":
            font_family = self._eastAsia or self._eastAsiaTheme
        else:
            font_family = self._cs or self._cstheme
        if isinstance(font_family, FontFamily):
            font: str | None = font_family.typeface
        else:
            font = font_family
        return font or default

    def _guess_slot(self, char: str) -> FontSlot:
        unicode = ord(char)
        for u_set, classificator in _CLASS_TABLE:
            if unicode in u_set:
                if isinstance(classificator, FontSlot):
                    font_slot = classificator
                else:
                    font_slot = classificator(self, unicode)
                if font_slot == "eastAsia" and self._hint == "eastAsia":
                    return FontSlot.EAST_ASIA
                elif (
                    self._ch_fmt._complex_script or self._ch_fmt.right_to_left
                ):
                    return FontSlot.COMPLEX_SCRIPT
                else:
                    return font_slot
        raise ValueError(f"No font slot for given char `{char}`")

    # TODO: idk how to implement it right (look deep in spec for supplemental fonts)
    def _theme_font(self, name: str) -> FontFamily | None:
        theme: SE_THEME | None = self._prop_resolved(name)
        if theme is None:
            return None
        theme_proxy = self.document_part.theme
        if theme in (SE_THEME.MAJOR_ASCII, SE_THEME.MAJOR_H_ANSI):
            return theme_proxy.major_latin
        elif theme == SE_THEME.MAJOR_EAST_ASIA:
            return theme_proxy.major_east_asia
        elif theme == SE_THEME.MAJOR_BIDI:
            return theme_proxy.major_complex_script
        elif theme in (SE_THEME.MINOR_ASCII, SE_THEME.MINOR_H_ANSI):
            return theme_proxy.minor_latin
        elif theme == SE_THEME.MINOR_EAST_ASIA:
            return theme_proxy.minor_east_asia
        else:
            return theme_proxy.minor_complex_script

    def _prop_resolved(self, name: str) -> Any:
        prop = self._ch_fmt._display(f"rPr.rFonts.{name}")
        if isinstance(prop, NotFound):
            return None
        return prop

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


_CLASS_TABLE: list[
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
