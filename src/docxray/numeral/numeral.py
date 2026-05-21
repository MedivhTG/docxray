import unicodedata
from functools import lru_cache
from typing import Literal

import homoglyphs
from unicode_rbnf.engine import RbnfEngine

from .bcp47 import script
from .charset import NAME_TO_CHARSET, CharsetName


class Numeral:
    """Class for translating ordinal position (int) to symbol from
    chosen word chracter set.

    `NOTE`:
        1) Some character sets are not fully supported or implemented for a while.
        2) Bullet character set is missing because it depends on hierarchy level.
    """

    @classmethod
    def decimal(cls, ord: int) -> str:
        cls._ord_validate(ord)
        return str(ord)

    @classmethod
    def upper_roman(cls, ord: int) -> str:
        return cls._roman(ord, CharsetName.UPPER_ROMAN)

    @classmethod
    def lower_roman(cls, ord: int) -> str:
        return cls._roman(ord, CharsetName.LOWER_ROMAN)

    @classmethod
    def upper_letter(cls, ord: int) -> str:
        return cls._letter(ord, CharsetName.UPPER_LETTER)

    @classmethod
    def lower_letter(cls, ord: int) -> str:
        return cls._letter(ord, CharsetName.LOWER_LETTER)

    @classmethod
    def ordinal(cls, ord: int, locale: str = "en-US") -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine(locale)
        return engine.format_number(ord, ruleset_names=["digits-ordinal"]).text

    @classmethod
    def cardinal_text(cls, ord: int, locale: str = "en-US") -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine(locale)
        return engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text

    @classmethod
    def ordinal_text(cls, ord: int, locale: str = "en-US") -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine(locale)
        return engine.format_number(
            ord, ruleset_names=["spellout-ordinal"]
        ).text

    @classmethod
    def hex(cls, ord: int) -> str:
        cls._ord_validate(ord)
        return format(ord, "X")

    @classmethod
    def chicago(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.CHICAGO)

    @classmethod
    def ideograph_digital(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.IDEOGRAPH_DIGITAL)

    # TODO: realize
    @classmethod
    def japanese_counting(cls, ord: int) -> str:
        raise NotImplementedError()

    @classmethod
    def aiueo(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.AIUEO)

    @classmethod
    def iroha(cls, ord: int) -> str:
        return cls._cyclic(ord, CharsetName.IROHA)

    @classmethod
    def decimal_full_width(cls, ord: int) -> str:
        return cls._decimal_full_width(ord, CharsetName.DECIMAL_FULL_WIDTH)

    @classmethod
    def decimal_half_width(cls, ord: int) -> str:
        return cls.decimal(ord)

    # TODO: realize
    @classmethod
    def japanese_legal(cls, ord: int) -> str:
        raise NotImplementedError()

    @classmethod
    def japanese_digital_ten_thousand(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.JAPANESE_DIGITAL_TEN_THOUSAND)

    @classmethod
    def decimal_enclosed_circle(cls, ord: int) -> str:
        return cls._decimal_fallback(ord, CharsetName.DECIMAL_ENCLOSED_CIRCLE)

    @classmethod
    def decimal_full_width_2(cls, ord: int) -> str:
        return cls._decimal_full_width(ord, CharsetName.DECIMAL_FULL_WIDTH_2)

    @classmethod
    def aiueo_full_width(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.AIUEO_FULL_WIDTH)

    @classmethod
    def iroha_full_width(cls, ord: int) -> str:
        return cls._cyclic(ord, CharsetName.IROHA_FULL_WIDTH)

    @classmethod
    def decimal_zero(cls, ord: int) -> str:
        decimal = cls.decimal(ord)
        if len(decimal) == 1:
            return f"0{decimal}"
        return decimal

    @classmethod
    def ganada(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.GANADA)

    @classmethod
    def chosung(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.CHOSUNG)

    @classmethod
    def decimal_enclosed_fullstop(cls, ord: int) -> str:
        return cls._decimal_fallback(
            ord, CharsetName.DECIMAL_ENCLOSED_FULLSTOP
        )

    @classmethod
    def decimal_enclosed_paren(cls, ord: int) -> str:
        return cls._decimal_fallback(ord, CharsetName.DECIMAL_ENCLOSED_PAREN)

    @classmethod
    def decimal_enclosed_circle_chinese(cls, ord: int) -> str:
        return cls._decimal_fallback(
            ord, CharsetName.DECIMAL_ENCLOSED_CIRCLE_CHINESE
        )

    @classmethod
    def ideograph_enclosed_circle(cls, ord: int) -> str:
        return cls._decimal_fallback(
            ord, CharsetName.IDEOGRAPH_ENCLOSED_CIRCLE
        )

    @classmethod
    def ideograph_traditional(cls, ord: int) -> str:
        return cls._decimal_fallback(ord, CharsetName.IDEOGRAPH_TRADITIONAL)

    @classmethod
    def ideograph_zodiac(cls, ord: int) -> str:
        return cls._decimal_fallback(ord, CharsetName.IDEOGRAPH_ZODIAC)

    @classmethod
    def ideograph_zodiac_traditional(cls, ord: int) -> str:
        return cls._cyclic(ord, CharsetName.IDEOGRAPH_ZODIAC_TRADITIONAL)

    # TODO: realize
    @classmethod
    def taiwanise_counting(cls, ord: int) -> str:
        raise NotImplementedError()

    # TODO: realize
    @classmethod
    def ideograph_legal_traditional(cls, ord: int) -> str:
        raise NotImplementedError()

    # TODO: realize
    @classmethod
    def taiwanese_counting_thousand(cls, ord: int) -> str:
        raise NotImplementedError()

    @classmethod
    def taiwanese_digital(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.TAIWANESE_DIGITAL)

    @classmethod
    def chinese_counting(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.CHINESE_COUNTING)

    # TODO: realize
    @classmethod
    def chinese_legal_simplified(cls, ord: int) -> str:
        raise NotImplementedError()

    # TODO: realize
    @classmethod
    def chinese_counting_thousand(cls, ord: int) -> str:
        raise NotImplementedError()

    @classmethod
    def korean_digital(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.KOREAN_DIGITAL)

    # TODO: realize
    @classmethod
    def korean_counting(cls, ord: int) -> str:
        raise NotImplementedError()

    # TODO: realize
    @classmethod
    def korean_legal(cls, ord: int) -> str:
        raise NotImplementedError()

    @classmethod
    def korean_digital_2(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.KOREAN_DIGITAL_2)

    @classmethod
    def vietnamese_counting(cls, ord: int) -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("vi-VN")
        return engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text

    @classmethod
    def russian_lower(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.RUSSIAN_LOWER)

    @classmethod
    def russian_upper(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.RUSSIAN_UPPER)

    @classmethod
    def none(cls) -> str:
        return ""

    @classmethod
    def number_in_dash(cls, ord: int) -> str:
        decimal = cls.decimal(ord)
        return f"-{decimal}-"

    # TODO: realize
    @classmethod
    def hebrew1(cls, ord: int) -> str:
        raise NotImplementedError()

    @classmethod
    def hebrew2(cls, ord: int) -> str:
        cls._ord_validate(ord)
        charset = cls._charset(ord, CharsetName.HEBREW_2)
        if ord <= len(charset):
            return charset[ord - 1]
        remainder = ord
        repeat = 0
        while remainder > len(charset):
            remainder -= len(charset)
            repeat += 1
        return charset[remainder - 1] + charset[-1] * repeat

    @classmethod
    def arabic_alpha(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.ARABIC_ALPHA)

    @classmethod
    def arabic_abjad(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.ARABIC_ABJAD)

    @classmethod
    def hindi_vowels(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.HINDI_VOWELS)

    @classmethod
    def hindi_consonants(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.HINDI_CONSONANTS)

    @classmethod
    def hindi_numbers(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.HINDI_NUMBERS)

    @classmethod
    def hindi_counting(cls, ord: int) -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("hi-IN")
        return engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text

    @classmethod
    def thai_letters(cls, ord: int) -> str:
        return cls._repeated(ord, CharsetName.THAI_LETTERS)

    @classmethod
    def thai_numbers(cls, ord: int) -> str:
        return cls._digital(ord, CharsetName.THAI_NUMBERS)

    @classmethod
    def thai_counting(cls, ord: int) -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("th-TH")
        return engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text

    @classmethod
    def baht_text(cls, ord: int) -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("th-TH")
        thai_number = engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text
        return f"{thai_number}บาทถ้วน"

    @classmethod
    def dollar_text(cls, ord: int, locale: str = "en-US") -> str:
        cls._ord_validate(ord)
        engine = cls._rbnf_engine(locale)
        cardinal = engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text
        return f"{cardinal} and 00/100"

    # TODO: i'm not sure what we must use, research later
    @classmethod
    def custom(cls, ord: int, pattern: str) -> str:
        cls._ord_validate(ord)
        return format(ord, pattern)

    @classmethod
    def _letter(
        cls,
        ord: int,
        letter_name: Literal[
            CharsetName.UPPER_LETTER, CharsetName.LOWER_LETTER
        ],
        locale: str = "en-US",
    ) -> str:
        if cls._is_latin_based(locale):
            cls._ord_validate(ord)
            case = (
                "upper" if letter_name == CharsetName.UPPER_LETTER else "lower"
            )
            charset = cls._alphabet(locale, case)
        else:
            charset = cls._charset(ord, letter_name)
        return cls._repeated_compute(ord, charset)

    @classmethod
    def _roman(
        cls,
        ord: int,
        roman_name: Literal[CharsetName.UPPER_ROMAN, CharsetName.LOWER_ROMAN],
    ) -> str:
        charset = cls._charset(ord, roman_name)
        I, V, X, L, C, D, M = charset  # noqa: E741
        RULES = [
            (1000, lambda: M),  # M
            (900, lambda: C + M),  # CM
            (500, lambda: D),  # D
            (400, lambda: C + D),  # CD
            (100, lambda: C),  # C
            (90, lambda: X + C),  # XC
            (50, lambda: L),  # L
            (40, lambda: X + L),  # XL
            (10, lambda: X),  # X
            (9, lambda: I + X),  # IX
            (5, lambda: V),  # V
            (4, lambda: I + V),  # IV
            (1, lambda: I),  # I
        ]
        REPEAT = (1000, 100, 10, 1)
        n = ord
        result = []
        for divisor, symbol_func in RULES:
            count = n // divisor
            if count > 0:
                if divisor in REPEAT:
                    # Repeating symbols (M, C, X, I)
                    result.append(symbol_func() * count)  # type: ignore[no-untyped-call]
                else:
                    # Single symbols (CM, D, CD, XC, L, XL, IX, V, IV)
                    result.append(symbol_func())  # type: ignore[no-untyped-call]
                n %= divisor
        return "".join(result)

    @classmethod
    def _repeated(cls, ord: int, charset_name: CharsetName) -> str:
        charset = cls._charset(ord, charset_name)
        return cls._repeated_compute(ord, charset)

    @classmethod
    def _cyclic(cls, ord: int, charset_name: CharsetName) -> str:
        charset = cls._charset(ord, charset_name)
        return cls._cyclic_compute(ord, charset)

    @classmethod
    def _digital(cls, ord: int, charset_name: CharsetName) -> str:
        if ord < 0:
            raise ValueError(f"Given ord `{ord}` is less than 0")
        charset = cls._charset(ord, charset_name, False)
        if ord == 0:
            return charset[ord]
        return cls._decimal_compute(ord, charset)

    @classmethod
    def _decimal_full_width(cls, ord: int, charset_name: CharsetName) -> str:
        if ord < 0:
            raise ValueError(f"Given ord `{ord}` is less than 0")
        charset = cls._charset(ord, charset_name, False)
        return cls._decimal_compute(ord, charset)

    @classmethod
    def _decimal_fallback(cls, ord: int, charset_name: CharsetName) -> str:
        charset = cls._charset(ord, charset_name)
        overhead = (ord - 1) // len(charset)
        if overhead > 0:
            return cls.decimal(ord)
        pos = ord - 1
        return charset[pos]

    @classmethod
    def _repeated_compute(cls, ord: int, charset: list[str]) -> str:
        repeat = (ord - 1) // len(charset)
        pos = (ord - 1) % len(charset)
        return charset[pos] * repeat

    @classmethod
    def _cyclic_compute(cls, ord: int, charset: list[str]) -> str:
        pos = (ord - 1) % len(charset)
        return charset[pos]

    @classmethod
    def _decimal_compute(cls, ord: int, charset: list[str]) -> str:
        digits = str(ord)
        return "".join(charset[int(d)] for d in digits)

    @classmethod
    def _charset(
        cls, ord: int, charset_name: CharsetName, validate_ord: bool = True
    ) -> list[str]:
        if validate_ord:
            cls._ord_validate(ord)
        charset = NAME_TO_CHARSET.get(charset_name)
        if charset is None:
            raise ValueError(f"No charset for given name {charset_name}")
        return charset

    @classmethod
    def _ord_validate(cls, ord: int) -> None:
        if ord < 1:
            raise ValueError(f"Given ord `{ord}` is less than 1")

    @classmethod
    @lru_cache
    def _alphabet(
        cls, locale: str = "en-US", case: Literal["lower", "upper"] = "upper"
    ) -> list[str]:
        code, _ = locale.split("-")
        alphabet = homoglyphs.Languages.get_alphabet([code])
        if case == "upper":
            return sorted(
                [chr for chr in alphabet if unicodedata.category(chr) == "Lu"]
            )
        return sorted(
            [chr for chr in alphabet if unicodedata.category(chr) == "Ll"]
        )

    @classmethod
    @lru_cache
    def _rbnf_engine(cls, locale: str = "en-US") -> RbnfEngine:
        locale_split = locale.split("-")
        if len(locale_split) == 2:
            code, _ = locale_split
        elif len(locale_split) == 1:
            code = locale_split[0]
        else:
            raise ValueError("No locale set")
        return RbnfEngine.for_language(code)

    @classmethod
    @lru_cache
    def _is_latin_based(cls, locale: str = "en-US") -> bool:
        return script(locale) == "Latn"
