from functools import cached_property

# docxray stuff
from docxray.enum.table import WD_CNF_FORMAT
from docxray.oxml.ns import W
from docxray.oxml.simpletypes import (
    ST_Cnf,
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
