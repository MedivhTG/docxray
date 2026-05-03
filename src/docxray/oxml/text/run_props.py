from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_OnOff, CT_String
from docxray.oxml.xmlchemy import OxmlElement


class CT_RPr(OxmlElement):
    @cached_property
    def i(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.I, CT_OnOff)

    @cached_property
    def rStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.R_STYLE, CT_String)
