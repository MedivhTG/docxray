from functools import cached_property

# docxray stuff
from docxray.oxml.transitional.ns import W
from docxray.oxml.transitional.shared import CT_Cnf
from docxray.oxml.transitional.xmlchemy import OxmlElement


class CT_TrPr(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)
