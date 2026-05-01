from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.xmlchemy import OxmlElement


class CT_I(OxmlElement):
    pass


class CT_RPr(OxmlElement):
    @cached_property
    def i(self) -> bool | None:
        return self.child_toggled(W.I)
