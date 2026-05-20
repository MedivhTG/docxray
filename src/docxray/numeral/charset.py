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
IROHA = [
    chr(0xFF72),
    chr(0xFF9B),
    chr(0xFF8A),
    chr(0xFF86),
    chr(0xFF8E),
    chr(0xFF8D),
    chr(0xFF84),
    chr(0xFF81),
    chr(0xFF98),
    chr(0xFF87),
    chr(0xFF99),
    chr(0xFF66),
    chr(0xFF9C),
    chr(0xFF76),
    chr(0xFF96),
    chr(0xFF80),
    chr(0xFF9A),
    chr(0xFF7F),
    chr(0xFF82),
    chr(0xFF88),
    chr(0xFF85),
    chr(0xFF97),
    chr(0xFF91),
    chr(0xFF73),
    chr(0x30F0),
    chr(0xFF89),
    chr(0xFF75),
    chr(0xFF78),
    chr(0xFF94),
    chr(0xFF8F),
    chr(0xFF79),
    chr(0xFF8C),
    chr(0xFF7A),
    chr(0xFF74),
    chr(0xFF83),
    chr(0xFF71),
    chr(0xFF7B),
    chr(0xFF77),
    chr(0xFF95),
    chr(0xFF92),
    chr(0xFF90),
    chr(0xFF7C),
    chr(0x30F1),
    chr(0xFF8B),
    chr(0xFF93),
    chr(0xFF7E),
    chr(0xFF7D),
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
    IROHA = "iroha"


NAME_TO_CHARSET = {
    CharsetName.AIUEO: AIUEO,
    CharsetName.DECIMAL: DECIMAL,
    CharsetName.UPPER_ROMAN: UPPER_ROMAN,
    CharsetName.LOWER_ROMAN: LOWER_ROMAN,
    CharsetName.UPPER_LETTER: UPPER_LETTER,
    CharsetName.LOWER_LETTER: LOWER_LETTER,
    CharsetName.CHICAGO: CHICAGO,
    CharsetName.IDEOGRAPH_DIGITAL: IDEOGRAPH_DIGITAL,
    CharsetName.IROHA: IROHA,
}
