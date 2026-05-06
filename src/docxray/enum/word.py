from enum import IntFlag
from typing import Literal, Self


class WD_CNF_FORMAT(IntFlag):
    # FirstRow
    FIRST_ROW = 1 << 0
    # LastRow
    LAST_ROW = 1 << 1
    # FirstColumn
    FIRST_COLUMN = 1 << 2
    # LastColumn
    LAST_COLUMN = 1 << 3
    # Band1Vertical
    ODD_VERTICAL_BAND = 1 << 4
    # Band2Vertical
    EVEN_VERTICAL_BAND = 1 << 5
    # Band1Horizontal
    ODD_HORIZONTAL_BAND = 1 << 6
    # Band2Horizontal
    EVEN_HORIZONTAL_BAND = 1 << 7
    # NE Cell (NE - NorthEast/TopRight)
    FIRST_ROW_LAST_COLUMN = 1 << 8
    # NW Cell (NW - NorthWest/TopLeft)
    FIRST_ROW_FIRST_COLUMN = 1 << 9
    # SE Cell (SE - SouthEast/BottomRight)
    LAST_ROW_LAST_COLUMN = 1 << 10
    # SW Cell (SW - SouthWest/BottomLeft)
    LAST_ROW_FIRST_COLUMN = 1 << 11

    @classmethod
    def ordered_flags(
        cls, order: Literal["lowest", "highest"] = "highest"
    ) -> list["WD_CNF_FORMAT"]:
        """Get flags in priority order.

        `highest` - first property that will override all others.

        `lowest` - standard inheritance (not recommended for fast resolve).
        """
        if order == "highest":
            return _PRIORITY_FLAGS
        return list(reversed(_PRIORITY_FLAGS))

    @classmethod
    def from_string(cls, string: str) -> Self:
        bit_mask = int(string[::-1], 2)
        return cls(bit_mask)


# Order from reversed -> from highest to lowest:
_PRIORITY_FLAGS = [
    WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN,
    WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN,
    WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN,
    WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN,
    WD_CNF_FORMAT.LAST_ROW,
    WD_CNF_FORMAT.FIRST_ROW,
    WD_CNF_FORMAT.LAST_COLUMN,
    WD_CNF_FORMAT.FIRST_COLUMN,
    WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND,
    WD_CNF_FORMAT.ODD_HORIZONTAL_BAND,
    WD_CNF_FORMAT.EVEN_VERTICAL_BAND,
    WD_CNF_FORMAT.ODD_VERTICAL_BAND,
]
