from __future__ import annotations

from enum import IntFlag
from typing import Literal, Self

from docxray.oxml.trans.st.enums import SE_Border

type CnfName = Literal[
    "firstRow",
    "lastRow",
    "firstCol",
    "lastCol",
    "band1Vert",
    "band2Vert",
    "band1Horz",
    "band2Horz",
    "nwCell",
    "neCell",
    "swCell",
    "seCell",
]


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
            return _CNF_PRIORITY
        return list(reversed(_CNF_PRIORITY))

    @classmethod
    def from_string(cls, string: str) -> Self:
        mask = int(string[::-1], 2)
        return cls(mask)

    def format_name(self) -> CnfName:
        return _CNF_NAMES[self]


_CNF_NAMES: dict[WD_CNF_FORMAT, CnfName] = {
    WD_CNF_FORMAT.FIRST_ROW: "firstRow",
    WD_CNF_FORMAT.LAST_ROW: "lastRow",
    WD_CNF_FORMAT.FIRST_COLUMN: "firstCol",
    WD_CNF_FORMAT.LAST_COLUMN: "lastCol",
    WD_CNF_FORMAT.ODD_VERTICAL_BAND: "band1Vert",
    WD_CNF_FORMAT.EVEN_VERTICAL_BAND: "band2Vert",
    WD_CNF_FORMAT.ODD_HORIZONTAL_BAND: "band1Horz",
    WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND: "band2Horz",
    WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN: "nwCell",
    WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN: "neCell",
    WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN: "swCell",
    WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN: "seCell",
}

# Order from reversed -> from highest to lowest:
_CNF_PRIORITY = [
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

type CnfLookName = Literal[
    "firstRow", "lastRow", "firstColumn", "lastColumn", "noHBand", "noVBand"
]


class WD_CNF_TABLE_LOOK(IntFlag):
    APPLY_FIRST_ROW = 0x0020
    APPLY_LAST_ROW = 0x0040
    APPLY_FIRST_COLUMN = 0x0080
    APPLY_LAST_COLUMN = 0x0100
    NO_ROW_BANDING = 0x0200
    NO_COLUMN_BANDING = 0x0400

    def has_format(self, name: CnfLookName) -> bool:
        flag = _CNF_LOOK_NAME_TO_MEMBER[name]
        return bool(self & flag)


_CNF_LOOK_NAME_TO_MEMBER = {
    "firstRow": WD_CNF_TABLE_LOOK.APPLY_FIRST_ROW,
    "lastRow": WD_CNF_TABLE_LOOK.APPLY_LAST_ROW,
    "firstColumn": WD_CNF_TABLE_LOOK.APPLY_FIRST_COLUMN,
    "lastColumn": WD_CNF_TABLE_LOOK.APPLY_LAST_COLUMN,
    "noHBand": WD_CNF_TABLE_LOOK.NO_ROW_BANDING,
    "noVBand": WD_CNF_TABLE_LOOK.NO_COLUMN_BANDING,
}

_SE_BORDER_TO_ECMA_NUMBER = {
    SE_Border.SINGLE: 1,
    SE_Border.THICK: 2,
    SE_Border.DOUBLE: 3,
    SE_Border.DOTTED: 4,
    SE_Border.DASHED: 5,
    SE_Border.DOT_DASH: 6,
    SE_Border.DOT_DOT_DASH: 7,
    SE_Border.TRIPLE: 8,
    SE_Border.THIN_THICK_SMALL_GAP: 9,
    SE_Border.THICK_THIN_SMALL_GAP: 10,
    SE_Border.THIN_THICK_THIN_SMALL_GAP: 11,
    SE_Border.THIN_THICK_MEDIUM_GAP: 12,
    SE_Border.THICK_THIN_MEDIUM_GAP: 13,
    SE_Border.THIN_THICK_THIN_MEDIUM_GAP: 14,
    SE_Border.THIN_THICK_LARGE_GAP: 15,
    SE_Border.THICK_THIN_LARGE_GAP: 16,
    SE_Border.THIN_THICK_THIN_LARGE_GAP: 17,
    SE_Border.WAVE: 18,
    SE_Border.DOUBLE_WAVE: 19,
    SE_Border.DASH_SMALL_GAP: 20,
    SE_Border.DASH_DOT_STROKED: 21,
    SE_Border.THREE_D_EMBOSS: 22,
    SE_Border.THREE_D_ENGRAVE: 23,
    SE_Border.OUTSET: 24,
    SE_Border.INSET: 25,
}

# In ECMA-376 count of lines not mentioned, so
# this is just my guess..
_SE_BORDER_TO_LINES_COUNT = {
    SE_Border.SINGLE: 1,
    SE_Border.THICK: 1,
    SE_Border.DOUBLE: 2,
    SE_Border.DOTTED: 1,
    SE_Border.DASHED: 1,
    SE_Border.DOT_DASH: 1,
    SE_Border.DOT_DOT_DASH: 1,
    SE_Border.TRIPLE: 3,
    SE_Border.THIN_THICK_SMALL_GAP: 2,
    SE_Border.THICK_THIN_SMALL_GAP: 2,
    SE_Border.THIN_THICK_THIN_SMALL_GAP: 3,
    SE_Border.THIN_THICK_MEDIUM_GAP: 2,
    SE_Border.THICK_THIN_MEDIUM_GAP: 2,
    SE_Border.THIN_THICK_THIN_MEDIUM_GAP: 3,
    SE_Border.THIN_THICK_LARGE_GAP: 2,
    SE_Border.THICK_THIN_LARGE_GAP: 2,
    SE_Border.THIN_THICK_THIN_LARGE_GAP: 3,
    SE_Border.WAVE: 1,
    SE_Border.DOUBLE_WAVE: 2,
    SE_Border.DASH_SMALL_GAP: 1,
    SE_Border.DASH_DOT_STROKED: 1,
    SE_Border.THREE_D_EMBOSS: 1,
    SE_Border.THREE_D_ENGRAVE: 1,
    SE_Border.OUTSET: 1,
    SE_Border.INSET: 1,
}
