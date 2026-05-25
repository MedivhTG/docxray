from datetime import datetime
from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.st.enums import (
    SE_JC,
    SE_TEXT_DIRECTION,
    SE_Border,
    SE_OnOff1,
    SE_TblWidth,
)
from docxray.oxml.trans.st.shared_common import (
    ST_Lang,
    ST_OnOff,
    ST_String,
)
from docxray.oxml.trans.st.wml import (
    ST_Border,
    ST_Cnf,
    ST_DateTime,
    ST_DecimalNumber,
    ST_Jc,
    ST_LongHexNumber,
    ST_MeasurementOrPercent,
    ST_TblWidth,
    ST_TextDirection,
)
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_String(OxmlElement):
    @cached_property
    def val(self) -> str:
        return self.attr_required(W.VAL, ST_String)


class CT_OnOff(OxmlElement):
    @cached_property
    def val(self) -> bool | None | SE_OnOff1:
        return self.attr_optional(W.VAL, ST_OnOff)


class CT_Fonts(OxmlElement):
    pass


class CT_Color(OxmlElement):
    pass


class CT_SignedTwipsMeasure(OxmlElement):
    pass


class CT_TextScale(OxmlElement):
    pass


class CT_HpsMeasure(OxmlElement):
    pass


class CT_SignedHpsMeasure(OxmlElement):
    pass


class CT_Highlight(OxmlElement):
    pass


class CT_TextEffect(OxmlElement):
    pass


class CT_Border(OxmlElement):
    @cached_property
    def val(self) -> SE_Border:
        return self.attr_required(W.VAL, ST_Border)

    # TODO: uncomment and do work
    # @cached_property
    # def color(self) -> Literal["auto"] | str | None:
    #     return self.attr_optional(W.COLOR, ST_HexColor)

    # @cached_property
    # def themeColor(self):
    #     return self.attr_optional(W.THEME_COLOR, ST_ThemeColor)

    # @cached_property
    # def themeTint(self):
    #     return self.attr_optional(W.THEME_TINT, ST_UcharHexNumber)

    # @cached_property
    # def themeShade(self):
    #     return self.attr_optional(W.THEME_SHADE, ST_UcharHexNumber)

    # @cached_property
    # def sz(self):
    #     return self.attr_optional(W.SZ, ST_EighthPointMeasure)

    # @cached_property
    # def space(self):
    #     return self.attr_optional(W.SPACE, ST_PointMeasure)

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


class CT_FitText(OxmlElement):
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
