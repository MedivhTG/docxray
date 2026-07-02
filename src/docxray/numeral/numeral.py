"""Module for getting character string by ordinal number for MS Word.

Primary use is for lists, such as paragraphs with numbering format.
"""

import unicodedata
from functools import lru_cache
from typing import Literal

import homoglyphs
import num2words
from jp_number import JpNumberParser
from unicode_rbnf.engine import RbnfEngine

from .bcp47 import script
from .charset import NAME_TO_CHARSET, CharsetName


class Numeral:
    """Class for translating ordinal position (int) to symbol from
    chosen word chracter set. `ord` param almost always an 1-based number.

    **Common use:**
    ```python
        letter = Numeral.upper_letter(1)
        print(letter) # will print `A`
        ordinal = Numeral.ordinal(1, "en-US")
        print(ordinal) # will print `1st`
    ```

    **NOTE**:
        1) Some methods like `ordinal` can return fallback decimals or other if not
        in site-package tables (third-party libraries).
    """

    JP_PARSER = JpNumberParser()

    @classmethod
    def decimal(cls, ord: int) -> str:
        """Get ordinal number (1, 2, 3, ...)."""
        cls._ord_validate(ord)
        return str(ord)

    @classmethod
    def upper_roman(cls, ord: int) -> str:
        """Get ordinal number in roman format in uppercase (I, II, III, IV, ..., XVIII, XIX, XX, XXI, ...)."""
        return cls._roman(ord, CharsetName.UPPER_ROMAN)

    @classmethod
    def lower_roman(cls, ord: int) -> str:
        """Get ordinal number in roman format in lowercase (i, ii, iii, iv, ..., xviii, xix, xx, xxi, ...)."""
        return cls._roman(ord, CharsetName.LOWER_ROMAN)

    @classmethod
    def upper_letter(cls, ord: int, locale: str = "en-US") -> str:
        """Get ordinal letter for chosen `locale` in uppercase (for `en-US`: A, B, C, ...)."""
        return cls._letter(ord, CharsetName.UPPER_LETTER, locale)

    @classmethod
    def lower_letter(cls, ord: int, locale: str = "en-US") -> str:
        """Get ordinal letter for chosen `locale` in lowercase (for `en-US`: a, b, c, ...)."""
        return cls._letter(ord, CharsetName.LOWER_LETTER, locale)

    # TODO: not all ordinals supported
    @classmethod
    def ordinal(cls, ord: int, locale: str = "en-US") -> str:
        """Get ordinal word number for chosen `locale` (for `en-US`: 1st, 2nd, 3rd, ...).

        **NOTE**: not all ordinal suppoerted.
        """
        cls._ord_validate(ord)
        code, _ = cls._locale_split(locale)
        word = Num2Word.ordinal_num(ord, code)
        if word is not None:
            return word
        # Stringify for safety
        return str(num2words.num2words(ord, lang=code, to="ordinal_num"))

    @classmethod
    def cardinal_text(cls, ord: int, locale: str = "en-US") -> str:
        """Get ordinal word as cardinal for chosen `locale` (for `en-US`: One, Two, Three, ...)."""
        cls._ord_validate(ord)
        code, _ = cls._locale_split(locale)
        # Stringify for safety
        return str(num2words.num2words(ord, lang=code, to="cardinal"))

    @classmethod
    def ordinal_text(cls, ord: int, locale: str = "en-US") -> str:
        """Get ordinal word as ordinal text for chosen `locale` (for `en-US`: first, second, third, ...)."""
        cls._ord_validate(ord)
        code, _ = cls._locale_split(locale)
        # Stringify for safety
        return str(num2words.num2words(ord, lang=code, to="ordinal"))

    @classmethod
    def hex(cls, ord: int) -> str:
        """Get ordinal number in hexadecimal format (9, A, B, ...)."""
        cls._ord_validate(ord)
        return format(ord, "X")

    @classmethod
    def chicago(cls, ord: int) -> str:
        """Get ordinal repeated character sequence (*, †, ‡, §, **, ††, ...)."""
        return cls._repeated(ord, CharsetName.CHICAGO)

    @classmethod
    def ideograph_digital(cls, ord: int) -> str:
        """Get ordinal decimal number in asian languages (一, 二, 三, ..., 八, 九, 一〇)."""
        return cls._digital(ord, CharsetName.IDEOGRAPH_DIGITAL)

    @classmethod
    def japanese_counting(cls, ord: int) -> str:
        """Get ordinal number in Japanese counting system.

        This system uses characters to represent numbers 1-9 and combines them with
        additional characters for powers of ten (10, 100, 1000).

        Examples:
            1 → 一
            5 → 五
            10 → 十
            15 → 十五
            20 → 二十
            25 → 二十五
            100 → 百
            150 → 百五十
            1000 → 千
            1500 → 千五百
            10000 → 一万
            100000 → 十万
            1000000 → 百万
            10000000 → 千万
            100000000 → 一億
        """
        cls._ord_validate(ord)
        return cls.JP_PARSER.number2kanji(ord).as_kanji or ""

    @classmethod
    def aiueo(cls, ord: int) -> str:
        """Get ordinal repeated character sequence in order hallf-width katakana (ｱ, ｲ, ｳ, ..., ｦ, ﾝ, ｱｱ, ｲｲ, ｳｳ, ...)."""
        return cls._repeated(ord, CharsetName.AIUEO)

    @classmethod
    def iroha(cls, ord: int) -> str:
        """Get ordinal cyclic repeated character sequence in iroha ordered katakana (ｲ, ﾛ, ﾊ, ..., ｽ, ﾝ, ｲ, ﾛ, ﾊ, ...)."""
        return cls._cyclic(ord, CharsetName.IROHA)

    @classmethod
    def decimal_full_width(cls, ord: int) -> str:
        """Get ordinal number as character sequence of full width arabic numeral (１, ２, ３, ..., ８, ９, １０, １１, １２, ...)."""
        return cls._digital(ord, CharsetName.DECIMAL_FULL_WIDTH)

    @classmethod
    def decimal_half_width(cls, ord: int) -> str:
        """Get ordinal number like `decimal` (1, 2, 3, ...)."""
        return cls.decimal(ord)

    @classmethod
    def japanese_legal(cls, ord: int) -> str:
        """Get ordinal number in Japanese legal counting system.

        This system uses formal/legal characters (daiji) for numbers 1-9 and
        combines them with additional characters for powers of ten.

        The characters used:
            1: 壱 (U+58F1)
            2: 弐 (U+5F10)
            3: 参 (U+53C2)
            4: 四 (U+56DB)
            5: 伍 (U+4F0D)
            6: 六 (U+516D)
            7: 七 (U+4E03)
            8: 八 (U+516B)
            9: 九 (U+4E5D)
            10: 拾 (U+62FE)
            100: 百 (U+767E)
            1000: 阡 (U+9621)
            10000: 萬 (U+842C)

        Examples:
            1 → 壱
            5 → 伍
            10 → 拾
            15 → 拾伍
            20 → 弐拾
            25 → 弐拾伍
            100 → 百
            150 → 百伍拾
            1000 → 阡
            1500 → 阡伍百
            10000 → 萬
            15000 → 萬伍阡
            100000 → 拾萬
            1000000 → 百萬
            10000000 → 阡萬
        """
        cls._ord_validate(ord)
        return cls.JP_PARSER.number2kanji(ord, "daiji").as_kanji or ""

    @classmethod
    def japanese_digital_ten_thousand(cls, ord: int) -> str:
        """Get ordinal decimal number in japanese digital ten thousand counting system (一, 二, 三, ..., 八, 九, 一〇, 一一, 一二, ...)."""
        return cls._digital(ord, CharsetName.JAPANESE_DIGITAL_TEN_THOUSAND)

    @classmethod
    def decimal_enclosed_circle(cls, ord: int) -> str:
        """Get ordinal decimal number in circle character with fallback to decimal characters (①, ②, ③, ..., ⑲, ⑳, 21, ...)."""
        return cls._decimal_fallback(ord, CharsetName.DECIMAL_ENCLOSED_CIRCLE)

    @classmethod
    def decimal_full_width_2(cls, ord: int) -> str:
        """Get ordinal number as character sequence of full width arabic numeral (１, ２, ３, ..., ８, ９, １０, １１, １２, ...)."""
        return cls._digital(ord, CharsetName.DECIMAL_FULL_WIDTH_2)

    @classmethod
    def aiueo_full_width(cls, ord: int) -> str:
        """Get ordinal repeated character sequence in order full-width katakana (ア, イ, ウ, ..., ヲ, ン, アア, イイ, ウウ, ...)."""
        return cls._repeated(ord, CharsetName.AIUEO_FULL_WIDTH)

    @classmethod
    def iroha_full_width(cls, ord: int) -> str:
        """Get ordinal cyclic repeated character sequence for full-width iroha ordered katakana (イ, ロ, ハ, ..., ス, ン, イ, ロ, ハ, ...)."""
        return cls._cyclic(ord, CharsetName.IROHA_FULL_WIDTH)

    @classmethod
    def decimal_zero(cls, ord: int) -> str:
        """Get ordnial decimal number with zero character on start for single chars (01, 02, 03, ..., 08, 09, 10, 11, ...)"""
        decimal = cls.decimal(ord)
        if len(decimal) == 1:
            return f"0{decimal}"
        return decimal

    @classmethod
    def ganada(cls, ord: int) -> str:
        """Get ordinal repeated character sequence in korean ganada numbering (가, 나, 다, ..., 파, 하, 가가, 나나, 다다, ...)."""
        return cls._repeated(ord, CharsetName.GANADA)

    @classmethod
    def chosung(cls, ord: int) -> str:
        """Get ordinal repeated character sequence in korean chosung numbering (ㄱ ,ㄴ ,ㄷ, ..., ㅍ, ㅎ, ㄱㄱ, ㄴㄴ, ㄷㄷ, ...)."""
        return cls._repeated(ord, CharsetName.CHOSUNG)

    @classmethod
    def decimal_enclosed_fullstop(cls, ord: int) -> str:
        """Get ordinal decimal number dotted character with fallback to decimal characters (⒈, ⒉, ⒊, ..., ⒚, ⒛, 21, ...)."""
        return cls._decimal_fallback(
            ord, CharsetName.DECIMAL_ENCLOSED_FULLSTOP
        )

    @classmethod
    def decimal_enclosed_paren(cls, ord: int) -> str:
        """Get ordinal decimal number in parenthesis character with fallback to decimal characters (⑴, ⑵, ⑶, ..., ⒆, ⒇, 21, 22, ...)."""
        return cls._decimal_fallback(ord, CharsetName.DECIMAL_ENCLOSED_PAREN)

    @classmethod
    def decimal_enclosed_circle_chinese(cls, ord: int) -> str:
        """Get ordinal decimal number in circle character with fallback to decimal characters (①, ②, ③, ..., ⑲, ⑳, 21, ...)."""
        return cls._decimal_fallback(
            ord, CharsetName.DECIMAL_ENCLOSED_CIRCLE_CHINESE
        )

    @classmethod
    def ideograph_enclosed_circle(cls, ord: int) -> str:
        """Get ordinal ideograph decimal number in circle character with fallback to decimal characters (㈠, ㈡, ㈢, ..., ㈨, ㈩, 11,12, ...)."""
        return cls._decimal_fallback(
            ord, CharsetName.IDEOGRAPH_ENCLOSED_CIRCLE
        )

    @classmethod
    def ideograph_traditional(cls, ord: int) -> str:
        """Get ordinal ideograph traditional decimal number character with fallback to decimal characters (甲, 乙, 丙, 丁, ..., 壬, 癸, 11, 12, ...)."""
        return cls._decimal_fallback(ord, CharsetName.IDEOGRAPH_TRADITIONAL)

    @classmethod
    def ideograph_zodiac(cls, ord: int) -> str:
        """Get ordinal ideograph zodiac decimal number character with fallback to decimal characters (子, 丑, 寅, ..., 戌, 亥, 13, 14, ...)."""
        return cls._decimal_fallback(ord, CharsetName.IDEOGRAPH_ZODIAC)

    @classmethod
    def ideograph_zodiac_traditional(cls, ord: int) -> str:
        """Get ordinal cyclic repeated chracter sequence for ideograph zodiac traditional characters (甲子, 乙丑, 丙寅, ..., 壬戌, 癸亥, 甲子, 乙丑, 丙寅, ...)"""
        return cls._cyclic(ord, CharsetName.IDEOGRAPH_ZODIAC_TRADITIONAL)

    @classmethod
    def taiwanise_counting(cls, ord: int) -> str:
        """Get ordinal number in Taiwanese counting system (一, 二, 三, …, 九, 十, 十一, 十二, ..., 十九, 二十, 二十一, ..., 九十九, 一○○, 一○一, ...)"""
        charset = cls._charset(ord, CharsetName.TAIWANESE_COUNTING)
        TEN = charset[-1]
        charset = charset[:-1]
        if ord <= 9:
            return charset[ord]
        if ord <= 99:
            tens = ord // 10
            ones = ord % 10
            if tens == 1:
                result = TEN
            else:
                result = charset[tens] + TEN
            if ones > 0:
                result += charset[ones]
            return result
        return "".join(charset[int(d)] for d in str(ord))

    @classmethod
    def ideograph_legal_traditional(cls, ord: int) -> str:
        """Get ordinal number in Traditional Legal Ideograph format."""
        cls._ord_validate(ord)
        digits = ["", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖"]
        TEN = "拾"
        HUNDRED = "佰"
        THOUSAND = "仟"
        TEN_THOUSAND = "萬"

        def convert_less_than_10000(n: int) -> str:
            if n == 0:
                return ""
            parts = []
            thousand = n // 1000
            if thousand > 0:
                parts.append(digits[thousand] + THOUSAND)
            n %= 1000
            hundred = n // 100
            if hundred > 0:
                parts.append(digits[hundred] + HUNDRED)
            n %= 100
            ten = n // 10
            if ten > 0:
                if ten == 1:
                    parts.append(TEN)
                else:
                    parts.append(digits[ten] + TEN)
            n %= 10
            if n > 0:
                parts.append(digits[n])
            return "".join(parts)

        if ord < 10000:
            return convert_less_than_10000(ord)
        ten_thousands = ord // 10000
        remainder = ord % 10000
        parts = []
        if ten_thousands > 0:
            if ten_thousands == 1:
                parts.append(TEN_THOUSAND)
            else:
                parts.append(
                    convert_less_than_10000(ten_thousands) + TEN_THOUSAND
                )
        if remainder > 0:
            parts.append(convert_less_than_10000(remainder))
        return "".join(parts)

    @classmethod
    def taiwanese_counting_thousand(cls, ord: int) -> str:
        """Get ordinal number in Taiwanese Counting Thousand System."""
        cls._ord_validate(ord)

        digits = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
        TEN = "十"
        HUNDRED = "百"
        THOUSAND = "千"
        TEN_THOUSAND = "萬"
        ZERO = "零"

        def convert_group(n: int, add_zero: bool = False) -> str:
            if n == 0:
                return ""
            parts = []
            original = n
            thousand = n // 1000
            if thousand > 0:
                parts.append(digits[thousand] + THOUSAND)
            elif add_zero and original >= 1000 and original % 1000 != 0:
                parts.append(ZERO)
            n %= 1000
            hundred = n // 100
            if hundred > 0:
                parts.append(digits[hundred] + HUNDRED)
            elif add_zero and original >= 100 and original % 100 != 0:
                parts.append(ZERO)
            n %= 100
            ten = n // 10
            if ten > 0:
                parts.append(digits[ten] + TEN)
            elif add_zero and original >= 10 and original % 10 != 0:
                parts.append(ZERO)
            n %= 10
            if n > 0:
                parts.append(digits[n])
            return "".join(parts)

        if ord <= 9:
            return digits[ord]
        if ord < 100:
            tens = ord // 10
            ones = ord % 10

            result = digits[tens] + TEN
            if ones > 0:
                result += digits[ones]
            return result
        if ord < 1000:
            hundreds = ord // 100
            remainder = ord % 100
            result = digits[hundreds] + HUNDRED
            if remainder == 0:
                return result
            if remainder < 10:
                result += ZERO + digits[remainder]
            else:
                tens = remainder // 10
                ones = remainder % 10
                result += digits[tens] + TEN
                if ones > 0:
                    result += digits[ones]
            return result
        if ord < 10000:
            thousands = ord // 1000
            remainder = ord % 1000

            result = digits[thousands] + THOUSAND

            if remainder == 0:
                return result
            if remainder < 100:
                result += ZERO + convert_group(remainder, False)
            else:
                result += convert_group(remainder, False)
            return result
        ten_thousands = ord // 10000
        remainder = ord % 10000
        parts = []
        if ten_thousands == 1:
            parts.append(TEN_THOUSAND)
        else:
            parts.append(convert_group(ten_thousands, False) + TEN_THOUSAND)
        if remainder > 0:
            if remainder < 1000:
                parts.append(ZERO + convert_group(remainder, False))
            else:
                parts.append(convert_group(remainder, False))

        return "".join(parts)

    @classmethod
    def taiwanese_digital(cls, ord: int) -> str:
        """Get ordinal decimal number in taiwanese digital counting system (一, 二, ..., 八, 九, 一○,一一, 一二, ...)."""
        return cls._digital(ord, CharsetName.TAIWANESE_DIGITAL)

    @classmethod
    def chinese_counting(cls, ord: int) -> str:
        """Get ordinal decimal number in chinese digital counting system (一, 二, 三, ..., 九, 十, 十一, 十二, ...)."""
        return cls._digital(ord, CharsetName.CHINESE_COUNTING)

    @classmethod
    def chinese_legal_simplified(cls, ord: int) -> str:
        """Get ordinal number in Chinese Legal Simplified format."""
        cls._ord_validate(ord)
        digits = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
        TEN = "拾"
        HUNDRED = "佰"
        THOUSAND = "仟"
        TEN_THOUSAND = "万"

        def convert_group(n: int, need_zero: bool = False) -> str:
            """Convert number < 10000 with proper zero handling."""
            if n == 0:
                return ""

            parts = []
            original = n
            thousand = n // 1000
            if thousand > 0:
                parts.append(digits[thousand] + THOUSAND)
            elif need_zero and original >= 1000 and original % 1000 != 0:
                parts.append(digits[0])
            n %= 1000
            hundred = n // 100
            if hundred > 0:
                parts.append(digits[hundred] + HUNDRED)
            elif need_zero and original >= 100 and original % 100 != 0:
                parts.append(digits[0])
            n %= 100
            ten = n // 10
            if ten > 0:
                parts.append(digits[ten] + TEN)
            elif need_zero and original >= 10 and original % 10 != 0:
                parts.append(digits[0])
            n %= 10
            if n > 0:
                parts.append(digits[n])
            return "".join(parts)

        if ord <= 9:
            return digits[ord]
        if ord < 100:
            tens = ord // 10
            ones = ord % 10
            result = digits[tens] + TEN
            if ones > 0:
                result += digits[ones]
            return result
        if ord < 1000:
            hundreds = ord // 100
            remainder = ord % 100

            result = digits[hundreds] + HUNDRED
            if remainder == 0:
                return result
            if remainder < 10:
                result += digits[0] + digits[remainder]
            else:
                tens = remainder // 10
                ones = remainder % 10
                result += digits[tens] + TEN
                if ones > 0:
                    result += digits[ones]
            return result
        if ord < 10000:
            thousands = ord // 1000
            remainder = ord % 1000

            result = digits[thousands] + THOUSAND
            if remainder == 0:
                return result
            if remainder < 100:
                result += digits[0] + convert_group(remainder, False)
            else:
                result += convert_group(remainder, False)
            return result
        ten_thousands = ord // 10000
        remainder = ord % 10000
        parts = []
        if ten_thousands == 1:
            parts.append(TEN_THOUSAND)
        else:
            parts.append(convert_group(ten_thousands, False) + TEN_THOUSAND)
        if remainder > 0:
            if remainder < 1000:
                parts.append(digits[0] + convert_group(remainder, False))
            else:
                parts.append(convert_group(remainder, False))
        return "".join(parts)

    @classmethod
    def chinese_counting_thousand(cls, ord: int) -> str:
        """Get ordinal number in Chinese Counting Thousand System."""
        cls._ord_validate(ord)

        digits = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
        TEN = "十"
        HUNDRED = "百"
        THOUSAND = "千"
        TEN_THOUSAND = "万"

        def convert_group(n: int) -> str:
            if n == 0:
                return ""
            parts = []
            thousand = n // 1000
            if thousand > 0:
                parts.append(digits[thousand] + THOUSAND)
            n %= 1000
            hundred = n // 100
            if hundred > 0:
                parts.append(digits[hundred] + HUNDRED)
            n %= 100
            ten = n // 10
            if ten > 0:
                parts.append(digits[ten] + TEN)
            n %= 10
            if n > 0:
                parts.append(digits[n])
            return "".join(parts)

        if ord <= 9:
            return digits[ord]
        if ord < 100:
            tens = ord // 10
            ones = ord % 10
            result = digits[tens] + TEN
            if ones > 0:
                result += digits[ones]
            return result
        if ord < 1000:
            hundreds = ord // 100
            remainder = ord % 100
            result = digits[hundreds] + HUNDRED
            if remainder > 0:
                result += convert_group(remainder)
            return result
        if ord < 10000:
            thousands = ord // 1000
            remainder = ord % 1000
            result = digits[thousands] + THOUSAND
            if remainder > 0:
                result += convert_group(remainder)
            return result
        ten_thousands = ord // 10000
        remainder = ord % 10000
        parts = []
        if ten_thousands == 1:
            parts.append(TEN_THOUSAND)
        else:
            parts.append(convert_group(ten_thousands) + TEN_THOUSAND)
        if remainder > 0:
            if remainder < 1000:
                parts.append(digits[0])
                parts.append(convert_group(remainder))
            else:
                parts.append(convert_group(remainder))
        return "".join(parts)

    @classmethod
    def korean_digital(cls, ord: int) -> str:
        """Get ordinal decimal number in korean digital counting system (일, 이, 삼, ..., 팔, 구, 일영, 일일, ...)."""
        return cls._digital(ord, CharsetName.KOREAN_DIGITAL)

    @classmethod
    def korean_counting(cls, ord: int) -> str:
        """Get ordinal number in Korean counting system."""
        cls._ord_validate(ord)
        digits = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
        TEN = "십"
        HUNDRED = "백"
        THOUSAND = "천"
        TEN_THOUSAND = "만"

        def convert_less_than_10000(n: int) -> str:
            if n == 0:
                return ""
            parts = []
            thousand = n // 1000
            if thousand > 0:
                parts.append(digits[thousand] + THOUSAND)
            n %= 1000
            hundred = n // 100
            if hundred > 0:
                parts.append(digits[hundred] + HUNDRED)
            n %= 100
            ten = n // 10
            if ten > 0:
                parts.append(digits[ten] + TEN)
            n %= 10
            if n > 0:
                parts.append(digits[n])
            return "".join(parts)

        if ord <= 9:
            return digits[ord]
        if ord < 20:
            ones = ord % 10
            if ones == 0:
                return TEN
            else:
                return TEN + digits[ones]
        if ord < 100:
            tens = ord // 10
            ones = ord % 10
            result = digits[tens] + TEN
            if ones > 0:
                result += digits[ones]
            return result
        if ord < 10000:
            return convert_less_than_10000(ord)
        ten_thousands = ord // 10000
        remainder = ord % 10000
        parts = []
        if ten_thousands == 1:
            parts.append(TEN_THOUSAND)
        else:
            parts.append(convert_less_than_10000(ten_thousands) + TEN_THOUSAND)
        if remainder > 0:
            parts.append(convert_less_than_10000(remainder))
        return "".join(parts)

    @classmethod
    def korean_legal(cls, ord: int) -> str:
        """Get ordinal number in Korean legal numbering system."""
        cls._ord_validate(ord)
        native = [
            "",
            "하나",
            "둘",
            "셋",
            "넷",
            "다섯",
            "여섯",
            "일곱",
            "여덟",
            "아홉",
        ]
        tens_words = {
            1: "열",
            2: "스물",
            3: "서른",
            4: "마흔",
            5: "쉰",
            6: "예순",
            7: "일흔",
            8: "여든",
            9: "아흔",
        }
        sino = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
        UNITS = {1: "", 10: "십", 100: "백", 1000: "천", 10000: "만"}

        def sino_convert(n: int, unit: int = 1) -> str:
            if n == 0:
                return ""
            parts = []
            for u in [1000, 100, 10, 1]:
                if n >= u:
                    digit = n // u
                    n %= u
                    if digit == 1 and u > 1:
                        parts.append(UNITS[u])
                    else:
                        parts.append(sino[digit] + UNITS[u])
            return "".join(parts)

        if ord <= 9:
            return native[ord]
        if ord < 100:
            tens = ord // 10
            ones = ord % 10

            result = tens_words[tens]
            if ones > 0:
                result += native[ones]
            return result
        if ord < 10000:
            return sino_convert(ord)
        ten_thousands = ord // 10000
        remainder = ord % 10000
        parts = []
        if ten_thousands == 1:
            parts.append("만")
        else:
            parts.append(sino_convert(ten_thousands) + "만")
        if remainder > 0:
            parts.append(sino_convert(remainder))
        return "".join(parts)

    @classmethod
    def korean_digital_2(cls, ord: int) -> str:
        """Get ordinal decimal number in korean alternate digital counting system (一, 二, 三, ..., 八, 九, 一零, 一一, ...)."""
        return cls._digital(ord, CharsetName.KOREAN_DIGITAL_2)

    @classmethod
    def vietnamese_counting(cls, ord: int) -> str:
        """Get ordinal number for vietnamese numerals (một, hai, ba, ...)"""
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("vi-VN")
        return engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text

    @classmethod
    def russian_lower(cls, ord: int) -> str:
        """Get ordinal repeated character sequence in lowercase russian alphabet (а, б, в, ..., ю, я, аа, бб, вв, ...)."""
        return cls._repeated(ord, CharsetName.RUSSIAN_LOWER)

    @classmethod
    def russian_upper(cls, ord: int) -> str:
        """Get ordinal repeated character sequence in uppercase russian alphabet (А, Б, В, ..., Ю, Я, АА, ББ, ВВ, ...)."""
        return cls._repeated(ord, CharsetName.RUSSIAN_UPPER)

    @classmethod
    def none(cls) -> str:
        """Return empty string."""
        return ""

    @classmethod
    def number_in_dash(cls, ord: int) -> str:
        """Get ordinal decimal number with dashes (-1-, -2-, -3-, ...)."""
        decimal = cls.decimal(ord)
        return f"-{decimal}-"

    @classmethod
    def hebrew1(cls, ord: int) -> str:
        """Get ordinal number in Hebrew letters system."""
        cls._ord_validate(ord)

        if ord > 9999:
            return str(ord)
        ones = ["", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"]
        tens = ["", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"]
        hundreds = ["", "ק", "ר", "ש", "ת", "ך", "ם", "ן", "ף", "ץ"]
        thousands = ["", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"]
        if ord == 15:
            return "טו"
        if ord == 16:
            return "טז"

        def convert_less_than_1000(n: int) -> str:
            if n == 0:
                return ""
            if n == 15:
                return "טו"
            if n == 16:
                return "טז"
            parts = []
            h = n // 100
            n %= 100
            if h > 0:
                parts.append(hundreds[h])
            t = n // 10
            o = n % 10
            if t > 0:
                parts.append(tens[t])
            if o > 0:
                parts.append(ones[o])
            return "".join(parts)

        thousands_digit = ord // 1000
        remainder = ord % 1000
        parts = []
        if thousands_digit > 0:
            parts.append(thousands[thousands_digit])
        if remainder > 0:
            parts.append(convert_less_than_1000(remainder))
        return "".join(parts)

    @classmethod
    def hebrew2(cls, ord: int) -> str:
        """Get ordinal number in character sequence of hebrew alphabet."""
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
        """Get ordinal repeated character sequence of arabic alphabet."""
        return cls._repeated(ord, CharsetName.ARABIC_ALPHA)

    @classmethod
    def arabic_abjad(cls, ord: int) -> str:
        """Get ordinal repeated character sequence of arabic abjad numerals."""
        return cls._repeated(ord, CharsetName.ARABIC_ABJAD)

    @classmethod
    def hindi_vowels(cls, ord: int) -> str:
        """Get ordinal repeated character sequence of hindi vowels (क, ख, ग, ..., स, ह, कक, खख, गग, ...)."""
        return cls._repeated(ord, CharsetName.HINDI_VOWELS)

    @classmethod
    def hindi_consonants(cls, ord: int) -> str:
        """Get ordinal repeated character sequence of hindi consonants (अ, आ, इ, ..., अं,अः, अअ, आआ, इइ, ...)."""
        return cls._repeated(ord, CharsetName.HINDI_CONSONANTS)

    @classmethod
    def hindi_numbers(cls, ord: int) -> str:
        """Get ordinal decimal number in hindi numbers (१, २, ३, ..., ८, ९, १०, ११, १२, ...)."""
        return cls._digital(ord, CharsetName.HINDI_NUMBERS)

    @classmethod
    def hindi_counting(cls, ord: int) -> str:
        """Get ordinal number in hindi counting system (एक, दो, तीन, चार, पााँच, छः, सात, आठ, नौ, दस, ...)."""
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("hi-IN")
        return engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text

    @classmethod
    def thai_letters(cls, ord: int) -> str:
        """Get ordinal repeated character sequence of thai letters (ก, ข, ค, ..., อ, ฮ, กก, ขข, คค, ...)."""
        return cls._repeated(ord, CharsetName.THAI_LETTERS)

    @classmethod
    def thai_numbers(cls, ord: int) -> str:
        """Get ordinal decimal number in hindi numbers (१, २, ३, ..., ८, ९, १०, ११, १२, ...)."""
        return cls._digital(ord, CharsetName.THAI_NUMBERS)

    @classmethod
    def thai_counting(cls, ord: int) -> str:
        """Get ordinal number in thai counting system (หนงึ่ , สอง, สาม, สี่, หา้ , หก, เจ็ด, แปด, เกา้ , สบิ , ...)."""
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("th-TH")
        return engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text

    @classmethod
    def baht_text(cls, ord: int) -> str:
        """Get ordinal number in thai counting system with บาทถ้วน appended (หน่งึ บาทถ้วน, สองบาทถ้วน, สามบาทถ้วน, ...)."""
        cls._ord_validate(ord)
        engine = cls._rbnf_engine("th-TH")
        thai_number = engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text
        return f"{thai_number}บาทถ้วน"

    @classmethod
    def dollar_text(cls, ord: int, locale: str = "en-US") -> str:
        """Get ordinal number in spcified locale as ordinal text with `and 00/100` appended (for `en-US`: one and 00/100, two and 00/100, three and 00/100)."""
        cls._ord_validate(ord)
        engine = cls._rbnf_engine(locale)
        cardinal = engine.format_number(
            ord, ruleset_names=["spellout-numbering", "spellout-cardinal"]
        ).text
        return f"{cardinal} and 00/100"

    @classmethod
    def _letter(
        cls,
        ord: int,
        letter_case: Literal[
            CharsetName.UPPER_LETTER, CharsetName.LOWER_LETTER
        ],
        locale: str = "en-US",
    ) -> str:
        """Get ordinal letter for chosen locale (for `en-US` and `LOWER_LETTER`: a, b, c, ...)

        Args:
            ord (int): 1-based number.
            letter_case (Literal[ CharsetName.UPPER_LETTER, CharsetName.LOWER_LETTER ]): uppercase or lowercase letter charset.
            locale (str, optional): Chosen locale for charset. Defaults to "en-US".

        Returns:
            str: Unicode character string.
        """
        if cls._is_latin_based(locale):
            cls._ord_validate(ord)
            case = (
                "upper" if letter_case == CharsetName.UPPER_LETTER else "lower"
            )
            charset = cls._alphabet(locale, case)
        else:
            charset = cls._charset(ord, letter_case)
        return cls._repeated_compute(ord, charset)

    @classmethod
    def _roman(
        cls,
        ord: int,
        roman_case: Literal[CharsetName.UPPER_ROMAN, CharsetName.LOWER_ROMAN],
    ) -> str:
        """Get ordinal roman character (for `UPPER_ROMAN`: I, II, III, IV, ..., XVIII, XIX, XX, XXI, ...)

        Args:
            ord (int): 1-based number.
            roman_case (Literal[CharsetName.UPPER_ROMAN, CharsetName.LOWER_ROMAN]): uppercase or lowercase roman charset.

        Returns:
            str: Unicode character string.
        """
        charset = cls._charset(ord, roman_case)
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
        """Get ordinal repeated character sequence (for `CHICAGO`: *, †, ‡, §, **, ††, ...)

        Args:
            ord (int): 1-based number.
            charset_name (CharsetName): Chosen charset.

        Returns:
            str: Unicode character string.
        """
        charset = cls._charset(ord, charset_name)
        return cls._repeated_compute(ord, charset)

    @classmethod
    def _cyclic(cls, ord: int, charset_name: CharsetName) -> str:
        """Get ordinal cyclic repeated character sequence (for `IROHA`: ｲ, ﾛ, ﾊ, ..., ｽ, ﾝ, ｲ, ﾛ, ﾊ, ...)

        Args:
            ord (int): 1-based number.
            charset_name (CharsetName): Chosen charset.

        Returns:
            str: Unicode character string.
        """
        charset = cls._charset(ord, charset_name)
        return cls._cyclic_compute(ord, charset)

    @classmethod
    def _digital(cls, ord: int, charset_name: CharsetName) -> str:
        """Get ordinal decimal number (for `IDEOGRAPH_DIGITAL`: 一, 二, 三, ..., 八, 九, 一〇, ...)

        First character in given charset must be representation of zero number.

        Args:
            ord (int): 0-based number.
            charset_name (CharsetName): Chosen charset.

        Raises:
            ValueError: If `ord` number is not 0-based.

        Returns:
            str: Unicode character string.
        """
        if ord < 0:
            raise ValueError(f"Given ord `{ord}` is less than 0")
        charset = cls._charset(ord, charset_name, False)
        return cls._decimal_compute(ord, charset)

    @classmethod
    def _decimal_fallback(cls, ord: int, charset_name: CharsetName) -> str:
        """Get ordinal number for given charset with decimal fallback (for `IDEOGRAPH_ENCLOSED_CIRCLE`: ㈠, ㈡, ㈢, ..., ㈨, ㈩, 11,12, ...)

        Args:
            ord (int): 1-based number.
            charset_name (CharsetName): Chosen charset.

        Returns:
            str: Unicode character string.
        """
        charset = cls._charset(ord, charset_name)
        overhead = (ord - 1) // len(charset)
        if overhead > 0:
            return cls.decimal(ord)
        pos = ord - 1
        return charset[pos]

    @classmethod
    def _repeated_compute(cls, ord: int, charset: list[str]) -> str:
        """Get repeated character string from given charset.

        Args:
            ord (int): 1-based number.
            charset (list[str]): List of given charaters.

        Returns:
            str: Unicode character string.
        """
        repeat = (ord - 1) // len(charset) + 1
        pos = (ord - 1) % len(charset)
        return charset[pos] * repeat

    @classmethod
    def _cyclic_compute(cls, ord: int, charset: list[str]) -> str:
        pos = (ord - 1) % len(charset)
        return charset[pos]

    @classmethod
    def _decimal_compute(cls, ord: int, charset: list[str]) -> str:
        """Get decimal representation from given charset.

        Args:
            ord (int): 1-based number.
            charset (list[str]): List of given characters.

        Returns:
            str: Unicode character string.
        """
        digits = str(ord)
        return "".join(charset[int(d)] for d in digits)

    @classmethod
    def _charset(
        cls, ord: int, charset_name: CharsetName, validate_ord: bool = True
    ) -> list[str]:
        """Get list of chracters from internal mapping.

        Args:
            ord (int): 1-based number.
            charset_name (CharsetName): Charset name.
            validate_ord (bool, optional): Validate `ord` for 1-base. Defaults to True.

        Raises:
            ValueError: Cannot get charset from given name.

        Returns:
            list[str]: _description_
        """
        if validate_ord:
            cls._ord_validate(ord)
        charset = NAME_TO_CHARSET.get(charset_name)
        if charset is None:
            raise ValueError(f"No charset for given name {charset_name}")
        return charset

    @classmethod
    def _ord_validate(cls, ord: int) -> None:
        """Validate ordinal number.

        Args:
            ord (int): 1-based number.

        Raises:
            ValueError: If given ord is less than 1.
        """
        if ord < 1:
            raise ValueError(f"Given ord `{ord}` is less than 1")

    @classmethod
    def _locale_split(cls, locale: str) -> tuple[str, str]:
        """Split locale on separate lang tags, e.g. "en-US" to ("en", "US").

        Args:
            locale (str): Given locale for splitting.

        Raises:
            ValueError: If format of an locale is wrong.

        Returns:
            tuple[str, str]: First and second tags of an splitted locale.
        """
        locale_split = locale.split("-")
        if len(locale_split) == 2:
            return locale_split[0], locale_split[1]
        elif len(locale_split) == 1:
            return locale_split[0], ""
        else:
            raise ValueError(f"Wrong locale `{locale}`")

    @classmethod
    @lru_cache
    def _in_private_use_char(cls, char_or_code: int | str) -> bool:
        """Check if characted or int code in PUA (private use area, e.g. reserved area for characters).

        Args:
            char_or_code (int | str): Character strin or int (Unicode) code.

        Returns:
            bool: If `char_or_code` in PUA.
        """
        if isinstance(char_or_code, str):
            code = ord(char_or_code)
        else:
            code = char_or_code
        if 0xE000 <= code <= 0xF8FF:
            return True
        if 0xF0000 <= code <= 0xFFFFD:
            return True
        if 0x100000 <= code <= 0x10FFFD:
            return True
        return False

    @classmethod
    @lru_cache
    def _alphabet(
        cls, locale: str = "en-US", case: Literal["lower", "upper"] = "upper"
    ) -> list[str]:
        """Get charset (alphabet) from given locale and letter case.

        Args:
            locale (str, optional): Given locale. Defaults to "en-US".
            case (Literal[&quot;lower&quot;, &quot;upper&quot;], optional): Charset case. Defaults to "upper".

        Returns:
            list[str]: List of unicode character strings.
        """
        code, _ = cls._locale_split(locale)
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
        """Get loaded RBNF (rule-based number formatting) engine.

        Ususalyy need to get numerals for given locale.

        Args:
            locale (str, optional): Given locale. Defaults to "en-US".

        Returns:
            RbnfEngine: RBNF engine instance.
        """
        code, _ = cls._locale_split(locale)
        return RbnfEngine.for_language(code)

    @classmethod
    @lru_cache
    def _is_latin_based(cls, locale: str = "en-US") -> bool:
        """Determine if goven locale is latin-based.

        Args:
            locale (str, optional): Given locale. Defaults to "en-US".

        Returns:
            bool: `True` if it's latin-based, else `False`.
        """
        return script(locale) == "Latn"


class Num2Word:
    """Helper class to get ordinal number."""

    @classmethod
    def ordinal_num(cls, ord: int, code: str) -> str | None:
        """Get ordinal number for given code.

        **NOTE**: for now only `ru` code is accessed.

        Args:
            ord (int): 1-based number.
            code (str): Language tag, e.g. `ru` for `ru-RU`.

        Returns:
            str | None: Ordinal number string or `None` if no ordinals for given code.
        """
        if code == "ru":
            return f"{ord}-й"
        return None
