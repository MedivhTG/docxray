from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_Cnf
from docxray.oxml.xmlchemy import OxmlElement


class CT_TrPrBase(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)


class CT_TrPr(CT_TrPrBase):
    pass
