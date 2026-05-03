from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.simpletypes import ST_OnOff, ST_String
from docxray.oxml.xmlchemy import OxmlElement


class CT_String(OxmlElement):
    @cached_property
    def val(self) -> str:
        return ST_String.validate(self.get(W.VAL))


class CT_OnOff(OxmlElement):
    def __bool__(self) -> bool:
        return self.val

    @cached_property
    def val(self) -> bool:
        val = self.get(W.VAL)
        if val is None:
            return True
        return ST_OnOff.validate(val)
