# docxray stuff
from docxray.numeral.numeral import Numeral
from docxray.oxml.trans.st.enums import SE_NUMBER_FORMAT

F = SE_NUMBER_FORMAT

NUMERAL_RULES = {
    F.DECIMAL: Numeral.decimal,
    F.UPPER_ROMAN: Numeral.upper_roman,
    F.LOWER_ROMAN: Numeral.lower_roman,
    F.UPPER_LETTER: Numeral.upper_letter,
    F.LOWER_LETTER: Numeral.lower_letter,
    F.ORDINAL: Numeral.ordinal,
    F.CARDINAL_TEXT: Numeral.cardinal_text,
    F.ORDINAL_TEXT: Numeral.ordinal_text,
    F.HEX: Numeral.hex,
    F.CHICAGO: Numeral.chicago,
    F.IDEOGRAPH_DIGITAL: Numeral.ideograph_digital,
    # TODO: after implement uncomment
    # F.JAPANESE_COUNTING: Numeral.japanese_counting,
    F.JAPANESE_COUNTING: Numeral.decimal,
    F.AIUEO: Numeral.aiueo,
    F.IROHA: Numeral.iroha,
    F.DECIMAL_FULL_WIDTH: Numeral.decimal_full_width,
    F.DECIMAL_HALF_WIDTH: Numeral.decimal_half_width,
    # TODO: after implement uncomment
    # F.JAPANESE_LEGAL: Numeral.japanese_legal,
    F.JAPANESE_LEGAL: Numeral.decimal,
    F.JAPANESE_DIGITAL_TEN_THOUSAND: Numeral.japanese_digital_ten_thousand,
    F.DECIMAL_ENCLOSED_CIRCLE: Numeral.decimal_enclosed_circle,
    F.DECIMAL_FULL_WIDTH_2: Numeral.decimal_full_width_2,
    F.AIUEO_FULL_WIDTH: Numeral.aiueo_full_width,
    F.IROHA_FULL_WIDTH: Numeral.iroha_full_width,
    F.DECIMAL_ZERO: Numeral.decimal_zero,
    F.GANADA: Numeral.ganada,
    F.CHOSUNG: Numeral.chosung,
    F.DECIMAL_ENCLOSED_FULLSTOP: Numeral.decimal_enclosed_fullstop,
    F.DECIMAL_ENCLOSED_PAREN: Numeral.decimal_enclosed_paren,
    F.DECIMAL_ENCLOSED_CIRCLE_CHINESE: Numeral.decimal_enclosed_circle_chinese,
    F.IDEOGRAPH_ENCLOSED_CIRCLE: Numeral.ideograph_enclosed_circle,
    F.IDEOGRAPH_TRADITIONAL: Numeral.ideograph_traditional,
    F.IDEOGRAPH_ZODIAC: Numeral.ideograph_zodiac,
    F.IDEOGRAPH_ZODIAC_TRADITIONAL: Numeral.ideograph_zodiac_traditional,
    # TODO: after implement uncomment
    # F.TAIWANESE_COUNTING: Numeral.taiwanise_counting
    F.TAIWANESE_COUNTING: Numeral.decimal,
    # TODO: after implement uncomment
    # F.IDEOGRAPH_LEGAL_TRADITIONAL: Numeral.ideograph_legal_traditional,
    F.IDEOGRAPH_LEGAL_TRADITIONAL: Numeral.decimal,
    # TODO: after implement uncomment
    # F.TAIWANESE_COUNTING_THOUSAND: Numeral.taiwanese_counting_thousand,
    F.TAIWANESE_COUNTING_THOUSAND: Numeral.decimal,
    F.TAIWANESE_DIGITAL: Numeral.taiwanese_digital,
    F.CHINESE_COUNTING: Numeral.chinese_counting,
    # TODO: after implement uncomment
    # F.CHINESE_LEGAL_SIMPLIFIED: Numeral.chinese_legal_simplified,
    F.CHINESE_LEGAL_SIMPLIFIED: Numeral.decimal,
    # TODO: after implement uncomment
    # F.CHINESE_COUNTING_THOUSAND: Numeral.chinese_counting_thousand,
    F.CHINESE_COUNTING_THOUSAND: Numeral.decimal,
    F.KOREAN_DIGITAL: Numeral.korean_digital,
    # TODO: after implement uncomment
    # F.KOREAN_COUNTING: Numeral.korean_counting,
    F.KOREAN_COUNTING: Numeral.decimal,
    # TODO: after implement uncomment
    # F.KOREAN_LEGAL: Numeral.korean_legal,
    F.KOREAN_LEGAL: Numeral.decimal,
    F.KOREAN_DIGITAL_2: Numeral.korean_digital_2,
    F.VIETNAMESE_COUNTING: Numeral.vietnamese_counting,
    F.RUSSIAN_LOWER: Numeral.russian_lower,
    F.RUSSIAN_UPPER: Numeral.russian_upper,
    F.NONE: Numeral.none,
    F.NUMBER_IN_DASH: Numeral.number_in_dash,
    # TODO: after implement uncomment
    # F.HEBREW_1: Numeral.hebrew1,
    F.HEBREW_1: Numeral.decimal,
    F.HEBREW_2: Numeral.hebrew2,
    F.ARABIC_ALPHA: Numeral.arabic_alpha,
    F.ARABIC_ABJAD: Numeral.arabic_abjad,
    F.HINDI_VOWELS: Numeral.hindi_vowels,
    F.HINDI_CONSONANTS: Numeral.hindi_consonants,
    F.HINDI_NUMBERS: Numeral.hindi_numbers,
    F.HINDI_COUNTING: Numeral.hindi_counting,
    F.THAI_LETTERS: Numeral.thai_letters,
    F.THAI_NUMBERS: Numeral.thai_numbers,
    F.THAI_COUNTING: Numeral.thai_counting,
    F.BAHT_TEXT: Numeral.baht_text,
    F.DOLLAR_TEXT: Numeral.dollar_text,
    F.CUSTOM: Numeral.custom,
}
NUMERAL_WITH_LOCALE = {
    F.ORDINAL,
    F.CARDINAL_TEXT,
    F.ORDINAL_TEXT,
    F.DOLLAR_TEXT,
    F.UPPER_LETTER,
    F.LOWER_LETTER,
}
NUMERAL_SPECIFIC = {F.NONE, F.BULLET, F.CUSTOM}
