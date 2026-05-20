from enum import StrEnum


def charset(start: int, end: int) -> list[str]:
    return [chr(code) for code in range(start, end + 1)]


# We do not need it in Numeral class, but for compatibility
DECIMAL = charset(0x0030, 0x0039)
UPPER_ROMAN = [
    chr(0x0049),
    chr(0x0056),
    chr(0x0058),
    chr(0x004C),
    chr(0x0043),
    chr(0x0044),
    chr(0x004D),
]
AIUEO = [
    *charset(0xFF71, 0xFF9D),
    chr(0xFF9D),
    chr(0xFF9D),
]


class Charset(StrEnum):
    DECIMAL = "decimal"
    UPPER_ROMAN = "upper_roman"
    AIUEO = "aiueo"


NAME_TO_CHARSET = {
    Charset.AIUEO: AIUEO,
    Charset.DECIMAL: DECIMAL,
    Charset.UPPER_ROMAN: UPPER_ROMAN,
}
