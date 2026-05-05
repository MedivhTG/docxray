from enum import IntEnum


class XML_POSITION(IntEnum):
    """Describes the position of an element relative to its siblings."""

    START = 0
    MIDDLE = 1
    END = 2
    ONE_ITEM = 3
