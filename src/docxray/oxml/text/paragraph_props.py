from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_String
from docxray.oxml.xmlchemy import OxmlElement


class CT_PStyle(CT_String):
    pass


class CT_PPr(OxmlElement):
    @cached_property
    def pStyle(self) -> CT_PStyle | None:
        return self.child_zero_or_first(W.R_STYLE, CT_PStyle)
