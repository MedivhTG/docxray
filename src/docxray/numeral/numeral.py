from .charset import NAME_TO_CHARSET, Charset


class Numeral:
    @classmethod
    def aiueo(cls, ord: int) -> str:
        return cls._cyclic(ord, Charset.AIUEO)

    @classmethod
    def _cyclic(cls, ord: int, charset_name: Charset) -> str:
        """Get symbol from charset by position.

        If ord is outside of charset index than ord is equal to
        the ramined of the division of charset length

        Args:
            ord (int): 1-based position of char in `charset`
            charset_name (Charset): Named charset saved in memory.
        """
        charset = NAME_TO_CHARSET.get(charset_name)
        if charset is None:
            raise ValueError("No charset for given name")
        if ord <= 0:
            raise ValueError("Given ord is less or equal than 0")
        ord_next = ord % len(charset)
        pos = ord_next - 1
        return charset[pos]
