from typing import Literal

from .bcp47 import BCP47
from .charset import (
    NAME_TO_CHARSET,
    UPPER_LETTER_LATIN,
    UPPER_LETTER_OTHER,
    CharsetName,
)


class Numeral:
    @classmethod
    def decimal(cls, ord: int) -> str:
        if ord < 1:
            raise ValueError(f"Given ord {ord} is less than 1")
        return str(ord)

    @classmethod
    def upper_roman(cls, ord: int) -> str:
        return cls._roman(ord, CharsetName.UPPER_ROMAN)

    @classmethod
    def lower_roman(cls, ord: int) -> str:
        return cls._roman(ord, CharsetName.LOWER_ROMAN)

    @classmethod
    def upper_letter(cls, ord: int, lang: str) -> str:
        if ord < 1:
            raise ValueError(f"Given ord {ord} is less than 1")
        if cls._is_latin_based(lang):
            charset = UPPER_LETTER_LATIN
        else:
            charset = UPPER_LETTER_OTHER
        pos = ord - 1
        repeat = pos // len(charset) + 1
        char = charset[pos % len(charset)]
        return char * repeat

    @classmethod
    def _is_latin_based(cls, lang: str) -> bool:
        return BCP47.script(lang) == "Latn"

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
    def _cyclic(cls, ord: int, charset_name: CharsetName) -> str:
        """Get symbol from charset by position.

        If ord is outside of charset index than ord is equal to
        the ramined of the division of charset length

        Args:
            ord (int): 1-based position of char in `charset`
            charset_name (Charset): Named charset saved in memory.
        """
        charset = cls._charset(ord, charset_name)
        ord_next = ord % len(charset)
        pos = ord_next - 1
        return charset[pos]

    @classmethod
    def _charset(
        cls, ord_validate: int, charset_name: CharsetName
    ) -> list[str]:
        if ord_validate < 1:
            raise ValueError(f"Given ord {ord_validate} is less than 1")
        charset = NAME_TO_CHARSET.get(charset_name)
        if charset is None:
            raise ValueError(f"No charset for given name {charset_name}")
        return charset
