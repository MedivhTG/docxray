from enum import IntFlag


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
