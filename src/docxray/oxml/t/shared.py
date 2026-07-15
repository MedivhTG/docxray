from datetime import datetime
from functools import cached_property

# docxray stuff
from docxray.oxml.t.ns import W
from docxray.oxml.t.st.enums import (
    SE_BORDER,
    SE_HEX_COLOR_AUTO,
    SE_HINT,
    SE_JC,
    SE_ON_OFF_1,
    SE_TEXT_DIRECTION,
    SE_THEME,
    SE_THEME_COLOR,
    SE_TblWidth,
)
from docxray.oxml.t.st.shared_common import (
    ST_Lang,
    ST_OnOff,
    ST_String,
)
from docxray.oxml.t.st.wml import (
    ST_Border,
    ST_Cnf,
    ST_DateTime,
    ST_DecimalNumber,
    ST_EighthPointMeasure,
    ST_HexColor,
    ST_Hint,
    ST_HpsMeasure,
    ST_Jc,
    ST_LongHexNumber,
    ST_MeasurementOrPercent,
    ST_PointMeasure,
    ST_SignedTwipsMeasure,
    ST_TblWidth,
    ST_TextDirection,
    ST_Theme,
    ST_ThemeColor,
    ST_UcharHexNumber,
)
from docxray.oxml.t.xmlchemy import OxmlElement


class CT_String(OxmlElement):
    @cached_property
    def val(self) -> str:
        return self.attr_required(W.VAL, ST_String)


class CT_OnOff(OxmlElement):
    @cached_property
    def val(self) -> bool | None | SE_ON_OFF_1:
        return self.attr_optional(W.VAL, ST_OnOff)


class CT_Fonts(OxmlElement):
    @cached_property
    def hint(self) -> SE_HINT | None:
        return self.attr_optional(W.HINT, ST_Hint)

    @cached_property
    def ascii(self) -> str | None:
        return self.attr_optional(W.ASCII, ST_String)

    @cached_property
    def hAnsi(self) -> str | None:
        return self.attr_optional(W.H_ANSI, ST_String)

    @cached_property
    def eastAsia(self) -> str | None:
        return self.attr_optional(W.EAST_ASIA, ST_String)

    @cached_property
    def cs(self) -> str | None:
        return self.attr_optional(W.CS, ST_String)

    @cached_property
    def asciiTheme(self) -> SE_THEME | None:
        return self.attr_optional(W.ASCII_THEME, ST_Theme)

    @cached_property
    def hAnsiTheme(self) -> SE_THEME | None:
        return self.attr_optional(W.H_ANSI_THEME, ST_Theme)

    @cached_property
    def eastAsiaTheme(self) -> SE_THEME | None:
        return self.attr_optional(W.EAST_ASIA_THEME, ST_Theme)

    @cached_property
    def cstheme(self) -> SE_THEME | None:
        return self.attr_optional(W.CSTHEME, ST_Theme)


class CT_Color(OxmlElement):
    @cached_property
    def val(self) -> SE_HEX_COLOR_AUTO | bytes:
        return self.attr_optional(W.VAL, ST_HexColor, SE_HEX_COLOR_AUTO.AUTO)

    @cached_property
    def themeColor(self) -> SE_THEME_COLOR | None:
        return self.attr_optional(W.THEME_COLOR, ST_ThemeColor)

    @cached_property
    def themeTint(self) -> bytes | None:
        return self.attr_optional(W.THEME_TINT, ST_UcharHexNumber)

    @cached_property
    def themeShade(self) -> bytes | None:
        return self.attr_optional(W.THEME_SHADE, ST_UcharHexNumber)


class CT_SignedTwipsMeasure(OxmlElement):
    @cached_property
    def val(self) -> int | str:
        return self.attr_required(W.VAL, ST_SignedTwipsMeasure)


class CT_HpsMeasure(OxmlElement):
    @cached_property
    def val(self) -> int | str:
        return self.attr_required(W.VAL, ST_HpsMeasure)


class CT_SignedHpsMeasure(OxmlElement):
    pass


class CT_Border(OxmlElement):
    @cached_property
    def val(self) -> SE_BORDER:
        return self.attr_required(W.VAL, ST_Border)

    @cached_property
    def color(self) -> SE_HEX_COLOR_AUTO | bytes:
        return self.attr_optional(W.COLOR, ST_HexColor, SE_HEX_COLOR_AUTO.AUTO)

    @cached_property
    def themeColor(self) -> SE_THEME_COLOR | None:
        return self.attr_optional(W.THEME_COLOR, ST_ThemeColor)

    @cached_property
    def themeTint(self) -> bytes | None:
        return self.attr_optional(W.THEME_TINT, ST_UcharHexNumber)

    @cached_property
    def themeShade(self) -> bytes | None:
        return self.attr_optional(W.THEME_SHADE, ST_UcharHexNumber)

    @cached_property
    def sz(self) -> int | None:
        return self.attr_optional(W.SZ, ST_EighthPointMeasure)

    @cached_property
    def space(self) -> int:
        return self.attr_optional(W.SPACE, ST_PointMeasure, 0)

    @cached_property
    def shadow(self) -> bool | None:
        return self.attr_optional(W.SHADOW, ST_OnOff)

    @cached_property
    def frame(self) -> bool | None:
        return self.attr_optional(W.FRAME, ST_OnOff)


class CT_TblWidth(OxmlElement):
    @cached_property
    def w(self) -> int | str | None:
        return self.attr_optional(W.W, ST_MeasurementOrPercent)

    @cached_property
    def type(self) -> SE_TblWidth | None:
        return self.attr_optional(W.TYPE, ST_TblWidth)


class CT_Shd(OxmlElement):
    pass


class CT_Jc(OxmlElement):
    @cached_property
    def val(self) -> SE_JC:
        return self.attr_required(W.VAL, ST_Jc)


class CT_Em(OxmlElement):
    pass


class CT_Language(OxmlElement):
    @cached_property
    def val(self) -> str | None:
        return self.attr_optional(W.VAL, ST_Lang)

    @cached_property
    def eastAsia(self) -> str | None:
        return self.attr_optional(W.EAST_ASIA, ST_Lang)

    @cached_property
    def bidi(self) -> str | None:
        return self.attr_optional(W.BIDI, ST_Lang)


class CT_EastAsianLayout(OxmlElement):
    pass


class CT_AltChunk(OxmlElement):
    pass


class CT_FramePr(OxmlElement):
    pass


class CT_TextDirection(OxmlElement):
    @cached_property
    def val(self) -> SE_TEXT_DIRECTION:
        return self.attr_required(W.VAL, ST_TextDirection)


class CT_SectPr(OxmlElement):
    pass


class CT_DecimalNumber(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(W.VAL, ST_DecimalNumber)


class CT_Cnf(OxmlElement):
    @cached_property
    def val(self) -> str:
        return self.attr_required(W.VAL, ST_Cnf)


class CT_Markup(OxmlElement):
    @cached_property
    def id(self) -> int:
        return self.attr_required(W.ID, ST_DecimalNumber)


class CT_LongHexNumber(OxmlElement):
    @cached_property
    def val(self) -> bytes:
        return self.attr_required(W.VAL, ST_LongHexNumber)


class CT_TrackChange(CT_Markup):
    @cached_property
    def author(self) -> str:
        return self.attr_required(W.AUTHOR, ST_String)

    @cached_property
    def date(self) -> datetime | None:
        return self.attr_optional(W.DATE, ST_DateTime)


class CT_Empty(OxmlElement):
    pass


class CT_Rel(OxmlElement):
    pass


class CT_Perm(OxmlElement):
    pass


class CT_PermStart(OxmlElement):
    pass


class CT_ProofErr(OxmlElement):
    pass
