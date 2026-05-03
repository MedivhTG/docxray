"""Enumerations related to styles."""

from enum import StrEnum


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
