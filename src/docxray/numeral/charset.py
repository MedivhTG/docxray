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
LOWER_ROMAN = [
    chr(0x0069),
    chr(0x0076),
    chr(0x0078),
    chr(0x006C),
    chr(0x0063),
    chr(0x0064),
    chr(0x006D),
]
UPPER_LETTER_LATIN = [
    *charset(0x0041, 0x005A),
    chr(0x00C6),
    chr(0x00D8),
    chr(0x00C5),
]
UPPER_LETTER_OTHER = charset(0x0041, 0x005A)
AIUEO = [
    *charset(0xFF71, 0xFF9D),
    chr(0xFF9D),
    chr(0xFF9D),
]


class CharsetName(StrEnum):
    DECIMAL = "decimal"
    UPPER_ROMAN = "upperRoman"
    LOWER_ROMAN = "lowerRoman"
    AIUEO = "aiueo"


NAME_TO_CHARSET = {
    CharsetName.AIUEO: AIUEO,
    CharsetName.DECIMAL: DECIMAL,
    CharsetName.UPPER_ROMAN: UPPER_ROMAN,
    CharsetName.LOWER_ROMAN: LOWER_ROMAN,
}
