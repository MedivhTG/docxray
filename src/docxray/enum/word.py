from enum import IntFlag, StrEnum
from typing import Literal


class WD_STYLE_TYPE(StrEnum):
    CHARACTER = "character"
    LIST = "numbering"
    PARAGRAPH = "paragraph"
    TABLE = "table"


class WD_TBL_STYLE_OVERRIDE_TYPE(StrEnum):
    WHOLE_TABLE = "wholeTable"
    FIRST_ROW = "firstRow"
    LAST_ROW = "lastRow"
    FIRST_COL = "firstCol"
    LAST_COL = "lastCol"
    BAND_1_VERT = "band1Vert"
    BAND_2_VERT = "band2Vert"
    BAND_1_HORZ = "band1Horz"
    BAND_2_HORZ = "band2Horz"
    NE_CELL = "neCell"
    NW_CELL = "nwCell"
    SE_CELL = "seCell"
    SW_CELL = "swCell"


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


class WD_MERGE(StrEnum):
    CONTINUE = "continue"
    RESTART = "restart"


class WD_VERTICAL_ALIGN_RUN(StrEnum):
    BASELINE = "baseline"
    SUPERSCRIPT = "superscript"
    SUBSCRIPT = "subscript"


class WD_UNDERLINE(StrEnum):
    SINGLE = "single"
    WORDS = "words"
    DOUBLE = "double"
    THICK = "thick"
    DOTTED = "dotted"
    DOTTED_HEAVY = "dottedHeavy"
    DASH = "dash"
    DASHED_HEAVY = "dashedHeavy"
    DASH_LONG = "dashLong"
    DASH_LONG_HEAVY = "dashLongHeavy"
    DOT_DASH = "dotDash"
    DASH_DOT_HEAVY = "dashDotHeavy"
    DOT_DOT_DASH = "dotDotDash"
    DASH_DOT_DOT_HEAVY = "dashDotDotHeavy"
    WAVE = "wave"
    WAVY_HEAVY = "wavyHeavy"
    WAVY_DOUBLE = "wavyDouble"
    NONE = "none"


class WD_MULTILEVEL_TYPE(StrEnum):
    SINGLE_LEVEL = "singleLevel"
    MULTILEVEL = "multilevel"
    HYBRID_MULTILEVEL = "hybridMultilevel"
