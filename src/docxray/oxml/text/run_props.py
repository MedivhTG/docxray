from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.simpletypes import ST_OnOff
from docxray.oxml.xmlchemy import OxmlElement


class OxmlToggled(OxmlElement):
    def __bool__(self) -> bool:
        return self.val

    @cached_property
    def val(self) -> bool:
        val = self.get(W.VAL)
        if val is None:
            return True
        return ST_OnOff.validate(val)


class CT_I(OxmlToggled):
    pass


class CT_RPr(OxmlElement):
    @cached_property
    def i(self) -> CT_I | None:
        return self.child_zero_or_one(W.I, CT_I)
