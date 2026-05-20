from .charset import NAME_TO_CHARSET, Charset


class Numeral:
    @classmethod
    def decimal(cls, ord: int) -> str:
        """Foolish method to validate decimals required in numbering format.

        Args:
            ord (int): 1-based position of char in decimal charset.

        Raises:
            ValueError: If given ord is less than 1.

        Returns:
            str: String representation of integer.
        """
        if ord < 1:
            raise ValueError(f"Given ord {ord} is less than 1")
        return str(ord)

    @classmethod
    def upper_roman(cls, ord: int) -> str:
        charset = cls._charset(ord, Charset.UPPER_ROMAN)
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
    def _cyclic(cls, ord: int, charset_name: Charset) -> str:
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
    def _charset(cls, ord_validate: int, charset_name: Charset) -> list[str]:
        if ord_validate < 1:
            raise ValueError(f"Given ord {ord_validate} is less than 1")
        charset = NAME_TO_CHARSET.get(charset_name)
        if charset is None:
            raise ValueError(f"No charset for given name {charset_name}")
        return charset
