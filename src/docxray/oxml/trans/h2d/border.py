from functools import cached_property
from typing import Literal

# docxray stuff
from docxray.oxml.trans.enums import _SE_BORDER_TO_ECMA_NUMBER
from docxray.oxml.trans.proxy.shared import ElementProxy, Length, Pt
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.types import ProvidesXmlPart
from docxray.oxml.trans.shared import CT_Border
from docxray.oxml.trans.st.enums import (
    SE_BORDER,
    SE_HEX_COLOR_AUTO,
)

from .colorize import Colorize

type _WhichBorder = Literal["cell", "table"]


class Border(ElementProxy[CT_Border]):
    @cached_property
    def which_border(self) -> _WhichBorder:
        if isinstance(self._parent, Cell):
            return "cell"
        return "table"

    @cached_property
    def border_type(self) -> SE_BORDER:
        return self.element.val

    @cached_property
    def size(self) -> Length | None:
        sz = self.element.sz
        if sz is None:
            return None
        if self._is_art_border:
            if sz < 1:
                return Pt(1)
            if sz > 31:
                return Pt(31)
            return Pt(sz)
        if sz < 2:
            return Pt(2 / 8)
        if sz > 96:
            return Pt(96 / 8)
        return Pt(sz / 8)

    @cached_property
    def final_color(self) -> str | None:
        color = self.element.color
        if isinstance(color, SE_HEX_COLOR_AUTO):
            return None
        theme_color = self.element.themeColor
        if theme_color:
            base_color = Colorize.theme_color(theme_color)
            if self.element.themeTint:
                return Colorize.apply_tint(
                    base_color, self.element.themeTint.hex()
                )
            elif self.element.themeShade:
                return Colorize.apply_shade(
                    base_color, self.element.themeShade.hex()
                )
            else:
                return base_color
        else:
            return f"#{color.hex()}"

    @cached_property
    def shadow(self) -> bool:
        if self.element.shadow is None:
            return False
        return self.element.shadow

    @cached_property
    def _is_art_border(self) -> bool:
        return self.border_type not in _SE_BORDER_TO_ECMA_NUMBER
