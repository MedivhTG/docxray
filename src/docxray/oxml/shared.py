from datetime import datetime
from functools import cached_property

# docxray stuff
from docxray.enum.word import WD_CNF_FORMAT
from docxray.oxml.ns import W
from docxray.oxml.simpletypes import (
    ST_Cnf,
    ST_DateTime,
    ST_DecimalNumber,
    ST_OnOff,
    ST_String,
)
from docxray.oxml.xmlchemy import OxmlElement


class CT_String(OxmlElement):
    @cached_property
    def val(self) -> str:
        return self.attr_required(W.VAL, ST_String)


class CT_OnOff(OxmlElement):
    def __bool__(self) -> bool:
        return self.val

    @cached_property
    def val(self) -> bool:
        return self.attr_optional(W.VAL, ST_OnOff, True)


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
    pass


class CT_Shd(OxmlElement):
    pass


class CT_FitText(OxmlElement):
    pass


class CT_Em(OxmlElement):
    pass


class CT_Language(OxmlElement):
    pass


class CT_EastAsianLayout(OxmlElement):
    pass


class CT_AltChunk(OxmlElement):
    pass


class CT_DecimalNumber(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(W.VAL, ST_DecimalNumber)


class CT_Cnf(OxmlElement):
    @cached_property
    def val(self) -> WD_CNF_FORMAT:
        return self.attr_required(W.VAL, ST_Cnf)


class CT_Markup(OxmlElement):
    @cached_property
    def id(self) -> int:
        return self.attr_required(W.ID, ST_DecimalNumber)


class CT_TrackChange(CT_Markup):
    @cached_property
    def author(self) -> str:
        return self.attr_required(W.AUTHOR, ST_String)

    @cached_property
    def date(self) -> datetime | None:
        return self.attr_optional(W.DATE, ST_DateTime)
