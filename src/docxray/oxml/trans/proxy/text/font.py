from __future__ import annotations

from collections.abc import Callable
from enum import StrEnum
from functools import cached_property
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


# TODO: implement ECMA-376 full logic here
# TODO: look for fonts inside of Theme
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

    def guess_slot(self, char: str) -> FontSlot:
        unicode = ord(char)
        for u_set, classificator in CLASS_TABLE:
            if unicode in u_set:
                if isinstance(classificator, FontSlot):
                    return classificator
                return classificator(self, char)
        raise ValueError(f"No font slot for given char `{char}`")

    def _prop_resolved(self, name: str) -> Any:
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

    def _high_ansi_or_east_asia_zh(self, unicode: int) -> FontSlot:
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


combined_set = (
    u_set(0x02B0, 0x02FF)
    | u_set(0x0300, 0x036F)
    | u_set(0x0370, 0x03CF)
    | u_set(0x0400, 0x04FF)
)

# TODO: extend
CLASS_TABLE: list[tuple[set[int], FontSlot | Callable]] = [
    # Basic Latin
    (u_set(0x0000, 0x007F), FontSlot.ASCII),
    # Latin-1 Supplement
    (u_set(0x00A0, 0x00FF), Font._latin_1_supplement_slot),
    # Latin Extended-A, Latin Extended-B, IPA Extensions
    (
        u_set(0x0100, 0x017F) | u_set(0x0180, 0x024F) | u_set(0x0250, 0x02AF),
        Font._high_ansi_or_east_asia_zh,
    ),
    # Spacing Modifier Letters, Combining Diacritical Marks, Greek, Cyrillic
    (
        u_set(0x02B0, 0x02FF)
        | u_set(0x0300, 0x036F)
        | u_set(0x0370, 0x03CF)
        | u_set(0x0400, 0x04FF),
        Font._high_ansi_or_east_asia,
    ),
]
