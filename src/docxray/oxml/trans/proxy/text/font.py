from __future__ import annotations

from enum import StrEnum
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.proxy.shared import ElementProxy
from docxray.oxml.trans.shared import CT_Fonts
from docxray.oxml.trans.text.run_props import CT_RPr

if TYPE_CHECKING:
    from docxray.oxml.trans.proxy.text.run import Run
    from docxray.oxml.trans.proxy.numbering.numbering import Level


class FontSlot(StrEnum):
    ASCII = "ascii"
    HIGH_ANSI = "hAnsi"
    EAST_ASIA = "eastAsia"
    COMPLEX_SCRIPT = "cs"


def unicode_set(start: int, end: int) -> set[int]:
    return set(range(start, end + 1))


def in_encoding(char: str, encoding: str) -> bool:
    try:
        char.encode(encoding)
        return True
    except UnicodeEncodeError:
        return False


_LATN_SUP_1_EAST_ASIA_EXC = (
    {0x00A1, 0x00A4, 0x00AA, 0x00AD, 0x00AF, 0x00D7, 0x00F7}
    | unicode_set(0x00A7, 0x00A8)
    | unicode_set(0x00B0, 0x00B4)
    | unicode_set(0x00B6, 0x00BA)
    | unicode_set(0x00BC, 0x00BF)
)
_LATN_SUP_1_EAST_ASIA_ZH_EXC = (
    unicode_set(0x00E0, 0x00E1)
    | unicode_set(0x00E8, 0x00EA)
    | unicode_set(0x00EC, 0x00ED)
    | unicode_set(0x00F2, 0x00F3)
    | unicode_set(0x00F9, 0x00FA)
    | {0x00FC}
)


# TODO: implement ECMA-376 full logic here
# TODO: use H2D module for resolving
# TODO: look for lang spec
class Font(ElementProxy[CT_Fonts]):
    @cached_property
    def parent(self) -> "Level | Run":
        return cast("Level | Run", self._parent)

    @cached_property
    def slot(self) -> FontSlot:
        return FontSlot.ASCII

    @cached_property
    def font_name(self) -> str:
        slot = self.slot
        if slot == FontSlot.ASCII:
            return self.element.ascii or "Symbol"
        return "Symbol"

    @cached_property
    def _rPr(self) -> CT_RPr | None:
        return self.parent.element.rPr

    @cached_property
    def _lang(self) -> str | None:
        if self._rPr is None:
            return None
        lang = self._rPr.lang
        if lang is None:
            return None
        return lang.val

    def guess_slot(self, char: str) -> FontSlot:
        unicode = ord(char)
        for u_set, classificator in CLASS_TABLE:
            if unicode in u_set:
                if isinstance(classificator, FontSlot):
                    return classificator
                return classificator(self, char)
        raise ValueError(f"No font slot for given char `{char}`")

    def _latin_1_supplement_slot(self, unicode: int) -> FontSlot:
        if self.element.hint == "eastAsia":
            if unicode in _LATN_SUP_1_EAST_ASIA_EXC:
                return FontSlot.EAST_ASIA
            if self._lang == "zh" and unicode in _LATN_SUP_1_EAST_ASIA_ZH_EXC:
                return FontSlot.EAST_ASIA
        return FontSlot.HIGH_ANSI

    def _high_ansi_or_east_asia_hard(self, unicode: int) -> FontSlot:
        if self.element.hint == "eastAsia":
            ch = chr(unicode)
            if (
                self._lang == "zh"
                or in_encoding(ch, "big5")
                or in_encoding(ch, "gb2312")
            ):
                return FontSlot.EAST_ASIA
        return FontSlot.HIGH_ANSI


# TODO: extend
CLASS_TABLE = [
    # Basic Latin
    (unicode_set(0x0000, 0x007F), FontSlot.ASCII),
    # Latin-1 Supplement
    (unicode_set(0x00A0, 0x00FF), Font._latin_1_supplement_slot),
    # Latin Extended-A, Latin Extended-B, IPA Extensions
    (
        unicode_set(0x0100, 0x017F)
        | unicode_set(0x0180, 0x024F)
        | unicode_set(0x0250, 0x02AF),
        Font._high_ansi_or_east_asia_hard,
    ),
]
