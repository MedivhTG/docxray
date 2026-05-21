import unicodedata
from functools import lru_cache
from typing import Literal

import homoglyphs
from unicode_rbnf.engine import RbnfEngine

from .bcp47 import script
from .charset import NAME_TO_CHARSET, CharsetName


class Numeral:
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
        if ord < 0:
            raise ValueError(f"Given ord `{ord}` is less than 0")
        charset = cls._charset(ord, CharsetName.DECIMAL_FULL_WIDTH, False)
        return cls._decimal_compute(ord, charset)

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
        charset = cls._charset(ord, CharsetName.DECIMAL_ENCLOSED_CIRCLE)
        overhead = (ord - 1) // len(charset)
        if overhead > 0:
            return cls.decimal(ord)
        pos = ord - 1
        return charset[pos]

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
    def _repeated_compute(cls, ord: int, charset: list[str]) -> str:
        repeat = (ord - 1) // len(charset)
        pos = (ord - 1) % len(charset)
        return charset[pos] * repeat

    @classmethod
    def _cyclic_compute(cls, ord: int, charset: list[str]) -> str:
        pos = (ord - 1) % len(charset)
        return charset[pos]

    @classmethod
    def _digital(cls, ord: int, charset_name: CharsetName) -> str:
        if ord < 0:
            raise ValueError(f"Given ord `{ord}` is less than 0")
        charset = cls._charset(ord, charset_name, False)
        if ord == 0:
            return charset[ord]
        return cls._decimal_compute(ord, charset)

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

    @lru_cache
    @classmethod
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

    @lru_cache
    @classmethod
    def _rbnf_engine(cls, locale: str = "en-US") -> RbnfEngine:
        code, _ = locale.split("-")
        return RbnfEngine.for_language(code)

    @lru_cache
    @classmethod
    def _is_latin_based(cls, locale: str = "en-US") -> bool:
        return script(locale) == "Latn"
