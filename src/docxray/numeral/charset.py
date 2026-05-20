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

CHICAGO = [chr(0x002A), chr(0x2020), chr(0x2021), chr(0x00A7)]
IDEOGRAPH_DIGITAL = [
    chr(0x3007),
    chr(0x4E00),
    chr(0x4E8C),
    chr(0x4E09),
    chr(0x56DB),
    chr(0x4E94),
    chr(0x516D),
    chr(0x4E03),
    chr(0x516B),
    chr(0x4E5D),
]
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
    CHICAGO = "chicago"
    IDEOGRAPH_DIGITAL = "ideographDigital"
    AIUEO = "aiueo"


NAME_TO_CHARSET = {
    CharsetName.AIUEO: AIUEO,
    CharsetName.DECIMAL: DECIMAL,
    CharsetName.UPPER_ROMAN: UPPER_ROMAN,
    CharsetName.LOWER_ROMAN: LOWER_ROMAN,
    CharsetName.UPPER_LETTER: UPPER_LETTER,
    CharsetName.LOWER_LETTER: LOWER_LETTER,
    CharsetName.CHICAGO: CHICAGO,
    CharsetName.IDEOGRAPH_DIGITAL: IDEOGRAPH_DIGITAL,
}
