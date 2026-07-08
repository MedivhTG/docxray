from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Literal, cast

# docxray stuff
from docxray.colorize import Colorize
from docxray.length import Length, Pt
from docxray.oxml.t.enums import (
    _SE_BORDER_TO_ECMA_NUMBER,
    _SE_BORDER_TO_LINES_COUNT,
)
from docxray.oxml.t.package import TransitionalPackage
from docxray.oxml.t.proxy.base import ElementProxy
from docxray.oxml.t.shared import CT_Border
from docxray.oxml.t.st.enums import SE_BORDER

if TYPE_CHECKING:
    from .table.cell import Cell

type _WhichParent = Literal["cell", "table"]


class Border(ElementProxy[CT_Border]):
    @classmethod
    def oppose(
        cls, side_1: Border | None, side_2: Border | None
    ) -> Border | None:
        """Determine which border-side must be rendered.

        From spec ECMA-376, Part 1, 17.4.66:
        1) If either conflicting table cell border is nil or none (no border),
        then the opposing border shall be displayed.
        2) If a cell border conflicts with a table border, the cell border always wins.
        3) Each border shall then be assigned a weight using the following formula,
        and the border value using this calculation shall be displayed over the alternative border =>
        `Wborder = # of lines in border ∗ border number`
        4) If the borders have an equal weight, than the higher of the two on this precedence list shall win:
        `_SE_BORDER_TO_ECMA_NUMBER`.

        Args:
            side_1 (Border | None): Opposed border-side.
            side_2 (Border | None): Opposed border-side.

        Returns:
            Border | None: Won opposed border-side (or None if passed `None`).
        """
        none = (SE_BORDER.NULL, SE_BORDER.NONE)
        # Our border ommitted - return opposed, same for opposed
        if side_1 is None:
            return side_2
        if side_2 is None:
            return side_1
        # Cell always wins
        if side_1._which_parent == "table":
            return side_2
        if side_2._which_parent == "table":
            return side_1
        # Render side that is not in none border types
        if side_1.border_type in none:
            return side_2
        elif side_2.border_type in none:
            return side_1
        # Compare weights
        return cls._which_heavier(side_1, side_2)

    @classmethod
    def _which_heavier(cls, side_1: Border, side_2: Border) -> Border:
        # Art borders
        if side_1._weight is None:
            return side_1
        if side_2._weight is None:
            return side_2
        # Common borders
        if side_1._weight > side_2._weight:
            return side_1
        elif side_1._weight < side_2._weight:
            return side_2
        side_1_n = _SE_BORDER_TO_ECMA_NUMBER[side_1.border_type]
        side_2_n = _SE_BORDER_TO_ECMA_NUMBER[side_2.border_type]
        if side_1_n <= side_2_n:
            return side_1
        return side_2

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
        palette = cast(
            "TransitionalPackage", self.part.package
        ).main_document_part.theme.palette

        return Colorize.colorize(
            self.element.color,
            self.element.themeColor,
            palette,
            self.element.themeTint,
            self.element.themeShade,
        )

    @cached_property
    def shadow(self) -> bool:
        if self.element.shadow is None:
            return False
        return self.element.shadow

    @property
    def _which_parent(self) -> _WhichParent:
        from .table.cell import Cell

        if isinstance(self._parent, Cell):
            return "cell"
        return "table"

    @cached_property
    def _weight(self) -> int | None:
        lines_count = _SE_BORDER_TO_LINES_COUNT.get(self.border_type)
        border_number = _SE_BORDER_TO_ECMA_NUMBER.get(self.border_type)
        if lines_count is None or border_number is None:
            return None
        return lines_count * border_number

    @cached_property
    def _is_art_border(self) -> bool:
        return self.border_type not in _SE_BORDER_TO_ECMA_NUMBER
