from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_String
from docxray.oxml.xmlchemy import OxmlElement


class CT_PPr(OxmlElement):
    @cached_property
    def pStyle(self) -> CT_String | None:
        return self.child_zero_or_first(W.P_STYLE, CT_String)
