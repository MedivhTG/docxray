from enum import StrEnum

AIUEO = [
    *[chr(code) for code in range(0xFF71, 0xFF9D)],
    chr(0xFF9D),
    chr(0xFF9D),
]


class Charset(StrEnum):
    AIUEO = "aiueo"


NAME_TO_CHARSET = {Charset.AIUEO: AIUEO}
