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
# Only latin
UPPER_LETTER = charset(0x0041, 0x005A)
LOWER_LETTER = charset(0x0061, 0x007A)
AIUEO = [
    *charset(0xFF71, 0xFF9D),
    chr(0xFF9D),
    chr(0xFF9D),
]


class CharsetName(StrEnum):
    DECIMAL = "decimal"
    UPPER_ROMAN = "upperRoman"
    LOWER_ROMAN = "lowerRoman"
    UPPER_LETTER = "upperLetter"
    LOWER_LETTER = "lowerLetter"
    AIUEO = "aiueo"


NAME_TO_CHARSET = {
    CharsetName.AIUEO: AIUEO,
    CharsetName.DECIMAL: DECIMAL,
    CharsetName.UPPER_ROMAN: UPPER_ROMAN,
    CharsetName.LOWER_ROMAN: LOWER_ROMAN,
    CharsetName.UPPER_LETTER: UPPER_LETTER,
    CharsetName.LOWER_LETTER: LOWER_LETTER,
}
