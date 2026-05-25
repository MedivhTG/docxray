from enum import StrEnum
from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.shared import ElementProxy
from docxray.oxml.trans.shared import CT_Fonts


class FontSlot(StrEnum):
    ASCII = "ascii"
    HIGH_ANSI = "hAnsi"
    EAST_ASIA = "eastAsia"
    COMPLEX_SCRIPT = "cs"


# TODO: implement ECMA-376 full logic here
class Font(ElementProxy[CT_Fonts]):
    @cached_property
    def slot(self) -> FontSlot:
        return FontSlot.ASCII

    @cached_property
    def font_name(self) -> str:
        slot = self.slot
        if slot == FontSlot.ASCII:
            return self.element.ascii or "Symbol"
        return "Symbol"
