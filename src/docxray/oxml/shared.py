from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.simpletypes import ST_OnOff, ST_String
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
